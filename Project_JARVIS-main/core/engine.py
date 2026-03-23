import os
import json
import re
from groq import Groq
from core.registry import SkillRegistry

class JarvisEngine:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = "llama-3.3-70b-versatile"
        
        self.system_instruction = (
            "You are Jarvis, an AI voice assistant deeply integrated into a user's Windows computer. "
            "You have direct access to their system and can perform actions. "
            "Never say you cannot access the device, or that you are a text-based AI. "
            "Keep your responses extremely short, conversational, and designed to be spoken aloud. "
            "Do not use markdown, formatting, or lists."
        )

    def run_conversation(self, user_prompt: str) -> str:
        # First, try pattern matching for common commands
        result = self._try_pattern_matching(user_prompt)
        if result:
            return result
        
        # If no pattern match, use AI for general conversation
        return self._query_ai(user_prompt)

    def _try_pattern_matching(self, user_prompt: str) -> str:
        """Try to match user input to known commands and execute them directly."""
        prompt_lower = user_prompt.lower().strip()
        
        # Open WhatsApp contact pattern (Must be before generic 'open app' matcher)
        if "contact" in prompt_lower and "open" in prompt_lower:
            match = re.search(r'open contact\s+([a-zA-Z0-9_\s]+)', prompt_lower)
            if not match:
                match = re.search(r'open\s+([a-zA-Z0-9_\s]+)\s+contact', prompt_lower)
            if match:
                recipient = match.group(1).replace("in whatsapp", "").strip()
                try:
                    result = self.registry.get_function("open_whatsapp_contact")(recipient=recipient)
                    parsed = json.loads(result)
                    return parsed.get("message", f"Opened contact {recipient}")
                except:
                    pass

        # Search and play music/videos patterns
        yt_match = re.search(r'(?i)\b(?:play|search for|search|find)\s+(.*?)(?:on youtube|$)', prompt_lower)
        if yt_match:
            search_term = yt_match.group(1).strip()
            # Ignore empty searches or generic terms indicating other commands
            if search_term and search_term not in ["video", "music", "song", "it", "that", "this"]:
                try:
                    result = self.registry.get_function("search_and_play")(query=search_term)
                    return json.loads(result).get("message", result)
                except:
                    pass
        
        # Open app patterns
        if any(word in prompt_lower for word in ["open", "launch", "start"]):
            app_name = None
            known_apps = ["whatsapp", "discord", "chrome", "firefox", "notepad", "calculator", 
                       "gmail", "outlook", "word", "excel", "photos", "vlc", "spotify", "youtube shorts", "youtube", "copilot", "store", "explorer"]
            
            for app in known_apps:
                if app in prompt_lower:
                    app_name = app
                    break
                    
            # Fix for common WhatsApp typos if not already matched
            if not app_name and any(typo in prompt_lower for typo in ["whtsapp", "wattsapp", "whatsap", "whatapp"]):
                app_name = "whatsapp"
            
            # If no known app matched, extract whatever comes after open/launch/start
            if not app_name:
                for phrase in ["open ", "launch ", "start "]:
                    if phrase in prompt_lower:
                        app_name = prompt_lower.split(phrase, 1)[1].strip()
                        break
                        
            if app_name:
                try:
                    result = self.registry.get_function("open_app")(app_name=app_name)
                    parsed = json.loads(result)
                    return parsed.get("action", parsed.get("message", result))
                except:
                    # Fallback if result is not json
                    return result
        
        # Close app patterns
        for phrase in ["close ", "shut down ", "shut ", "exit ", "quit "]:
            if phrase in prompt_lower:
                if "all" in prompt_lower:
                    result = self.registry.get_function("close_app")(app_name="all")
                    return json.loads(result).get("message", result)
                
                app_name = prompt_lower.split(phrase, 1)[1].strip()
                if app_name:
                    result = self.registry.get_function("close_app")(app_name=app_name)
                    return json.loads(result).get("message", result)
        
        # Send message patterns
        if any(w in prompt_lower for w in ["send", "email", "gmail", "whatsapp", "message"]):
            # Default to whatsapp if just "send message" is used
            platform = "whatsapp" if "whatsapp" in prompt_lower else ("gmail" if any(w in prompt_lower for w in ["gmail", "email", "mail"]) else "whatsapp")
            
            if platform:
                # 1. Try matching WITH a message
                match = re.search(r'(?i)to\s+([a-zA-Z0-9_.@\s]+?)\s+(?:saying|that|with message|telling(?: him| her| them)?|about|message is|and tell(?: him| her| them)?)\s+(.*)', prompt_lower)
                if match:
                    recipient = match.group(1).strip()
                    message = match.group(2).strip()
                else:
                    # 2. Try matching WITHOUT a message (just open composer)
                    match2 = re.search(r'(?i)to\s+([a-zA-Z0-9_.@\s]+)', prompt_lower)
                    if match2:
                        recipient = match2.group(1).strip()
                        message = ""
                    else:
                        recipient = ""
                        message = ""
                
                if recipient:
                    try:
                        result = self.registry.get_function("send_message")(platform=platform, recipient=recipient, message=message)
                        return json.loads(result).get("message", result)
                    except:
                        pass
        
        # Website patterns
        if any(phrase in prompt_lower for phrase in ["open ", "go to ", "visit "]):
            for site in ["youtube", "google", "facebook", "instagram", "twitter", "reddit"]:
                if site in prompt_lower:
                    result = self.registry.get_function("open_website")(url=site)
                    return json.loads(result).get("action", result)
        
        # Screenshot
        if "screenshot" in prompt_lower or "capture" in prompt_lower:
            result = self.registry.get_function("take_screenshot")()
            return json.loads(result).get("message", result)
            
        # Clear text pattern
        if any(phrase in prompt_lower for phrase in ["clear message", "clear text", "clear the message", "clear the lines", "clear that", "clear chat", "clear", "clear it", "clear this"]):
            try:
                import time
                self.registry.get_function("keyboard_press")(keys="ctrl+a")
                time.sleep(0.1)
                self.registry.get_function("keyboard_press")(keys="backspace")
                return "Message cleared."
            except:
                pass
        
        # Unified app control patterns (pause, volume, close, fullscreen, etc.)
        if any(phrase in prompt_lower for phrase in ["pause", "stop", "play", "resume", "volume", "mute", "close tab", "close", "fullscreen", "exit", "skip", "next", "forward", "rewind", "back", "previous"]):
            # Extract the command
            command = None
            
            if any(w in prompt_lower for w in ["pause", "stop", "stop video"]):
                if "youtube" in prompt_lower:
                    try:
                        self.registry.get_function("keyboard_press")(keys="k")
                        return "Paused YouTube."
                    except: pass
                command = "pause"
            elif any(w in prompt_lower for w in ["play", "resume", "start"]):
                if "youtube" in prompt_lower:
                    try:
                        self.registry.get_function("keyboard_press")(keys="k")
                        return "Playing YouTube."
                    except: pass
                command = "play"
            elif any(w in prompt_lower for w in ["volume up", "increase volume", "louder"]):
                if "youtube" in prompt_lower:
                    try:
                        result = self.registry.get_function("youtube_control")(action="volume_up")
                        return json.loads(result).get("message", result)
                    except: pass
                command = "volume_up"
            elif any(w in prompt_lower for w in ["volume down", "decrease volume", "quieter"]):
                if "youtube" in prompt_lower:
                    try:
                        result = self.registry.get_function("youtube_control")(action="volume_down")
                        return json.loads(result).get("message", result)
                    except: pass
                command = "volume_down"
            elif "mute" in prompt_lower:
                command = "mute"
            elif any(w in prompt_lower for w in ["skip", "next track", "next video", "skip ad"]):
                command = "skip"
            elif any(w in prompt_lower for w in ["forward", "fast forward", "skip forward"]):
                command = "forward"
            elif any(w in prompt_lower for w in ["rewind", "go back", "previous track", "back"]):
                command = "rewind"
            elif any(w in prompt_lower for w in ["close tab", "close this tab", "close app", "close the app", "close"]):
                command = "close"
            elif "fullscreen" in prompt_lower:
                command = "fullscreen"
            elif any(w in prompt_lower for w in ["exit", "quit"]):
                command = "exit"
            
            if command:
                try:
                    result = self.registry.get_function("app_control")(command=command)
                    return json.loads(result).get("message", result)
                except:
                    pass

        prompt_clean = re.sub(r'[^\w\s]', '', prompt_lower).strip()
        
        # Type message pattern (flexible: 'please type hello', 'type this is a test')
        type_match = re.search(r'(?i)\b(?:type|write)\s+(.*)', prompt_clean)
        if type_match:
            msg = type_match.group(1).strip()
            if msg:
                try:
                    self.registry.get_function("keyboard_type")(text=msg)
                    return "Message typed."
                except:
                    pass

        # Standalone "send" command to just press Enter (flexible format)
        if any(w in prompt_clean for w in ["send", "submit", "hit enter", "press enter"]):
            # If it's a short phrase like "please send", "just send it"
            if len(prompt_clean.split()) < 6 and "message to" not in prompt_clean:
                try:
                    self.registry.get_function("keyboard_press")(keys="enter")
                    return "Sent."
                except:
                    pass

        # Press key pattern
        if prompt_lower.startswith("press "):
            key = prompt_lower[6:].strip()
            try:
                self.registry.get_function("keyboard_press")(keys=key)
                return f"Pressed {key}."
            except:
                pass
        
        return None

    def _query_ai(self, user_prompt: str) -> str:
        """Query AI for general questions and conversation."""
        messages = [
            {"role": "system", "content": self.system_instruction},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=300
            )
            
            return response.choices[0].message.content
                
        except Exception as e:
            print(f"Groq API Error: {e}")
            return "I encountered an error. Please try again."
