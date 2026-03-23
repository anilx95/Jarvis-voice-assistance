import os
import sys
import json
import subprocess
import webbrowser
from typing import List, Dict, Any, Callable
from core.skill import Skill

class SystemSkill(Skill):
    """Skill for system operations: opening apps, sending messages, etc."""
    
    @property
    def name(self) -> str:
        return "system_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "open_app",
                    "description": "Open an application (e.g., notepad, calculator, WhatsApp, Gmail, Chrome, etc.)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {
                                "type": "string",
                                "description": "Name of the application to open (e.g., 'notepad', 'whatsapp', 'gmail', 'chrome')"
                            }
                        },
                        "required": ["app_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "close_app",
                    "description": "Close an application or all applications",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {
                                "type": "string",
                                "description": "Name of the application to close, or 'all' to close all open applications"
                            }
                        },
                        "required": ["app_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_message",
                    "description": "Send a message to a contact via WhatsApp or email via Gmail",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "platform": {
                                "type": "string",
                                "description": "Platform to use: 'whatsapp', 'gmail', 'email'"
                            },
                            "recipient": {
                                "type": "string",
                                "description": "Contact name or email address"
                            },
                            "message": {
                                "type": "string",
                                "description": "Message content to send"
                            }
                        },
                        "required": ["platform", "recipient", "message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_website",
                    "description": "Open a website in browser",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "Website URL or site name (e.g., 'google', 'youtube', 'facebook')"
                            }
                        },
                        "required": ["url"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "take_screenshot",
                    "description": "Take a screenshot of the screen",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_and_play",
                    "description": "Search for and play a song, video, or media on YouTube",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Song name, artist, video name, or search term"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "control_volume",
                    "description": "Control video/system volume (increase or decrease)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "Action: 'increase', 'decrease', or 'mute'"
                            }
                        },
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "pause_video",
                    "description": "Pause or stop the currently playing video",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "close_tab",
                    "description": "Close the current browser tab",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "app_control",
                    "description": "Unified app control: pause, play, volume, close, fullscreen, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Control command: pause, play, resume, stop, volume_up, volume_down, mute, close, fullscreen, exit"
                            }
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "keyboard_press",
                    "description": "Press one or more keyboard keys (e.g., 'enter', 'space', 'k', 'ctrl+c', 'alt+tab', 'win+d'). Use this for YouTube play/pause (k or space), window switching, or closing apps (alt+f4)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keys": {
                                "type": "string",
                                "description": "Key or keys to press. For combinations use '+' (e.g., 'ctrl+c')"
                            }
                        },
                        "required": ["keys"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "keyboard_type",
                    "description": "Type the given text string using the keyboard, as if a human is typing it. Useful for entering text into focused search bars or documents.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text string to type out"
                            }
                        },
                        "required": ["text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "mouse_control",
                    "description": "Control the mouse to click or move.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "Mouse action: 'left_click', 'right_click', 'double_click'"
                            }
                        },
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "youtube_control",
                    "description": "Control YouTube playback: speed (2x, 1.5x, normal), quality, volume (increase, decrease), skip, rewind",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "Action to perform: 'speed_up', 'speed_down', 'normal_speed', 'volume_up', 'volume_down', 'quality', 'skip_ad', 'fullscreen'"
                            }
                        },
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "gmail_control",
                    "description": "Control Gmail actions like compose, inbox, unread, spam, send, undo, redo, and selecting messages",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "Action to perform: 'compose', 'inbox', 'unread', 'spam', 'send', 'undo', 'redo', 'select_all'"
                            }
                        },
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_files",
                    "description": "Search for files on the local computer using Windows Search / File Explorer",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The file or folder name to search for"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "open_app": self.open_app,
            "close_app": self.close_app,
            "send_message": self.send_message,
            "open_website": self.open_website,
            "take_screenshot": self.take_screenshot,
            "search_and_play": self.search_and_play,
            "control_volume": self.control_volume,
            "pause_video": self.pause_video,
            "close_tab": self.close_tab,
            "app_control": self.app_control,
            "keyboard_press": self.keyboard_press,
            "keyboard_type": self.keyboard_type,
            "mouse_control": self.mouse_control,
            "open_whatsapp_contact": self.open_whatsapp_contact,
            "youtube_control": self.youtube_control,
            "gmail_control": self.gmail_control,
            "search_files": self.search_files
        }

    def open_app(self, app_name: str) -> str:
        """Open an application reliably using direct execution or Windows Search."""
        try:
            import pyautogui
            import time
            app_name_lower = app_name.lower().strip()
            
            # Map specific web apps to browsers
            if app_name_lower in ["youtube", "youtube shorts", "shorts", "gmail", "facebook", "twitter", "instagram"]:
                return self.open_website(app_name_lower)
                
            # Dictionary mapping common app names to executable commands
            direct_launch_map = {
                "chrome": "start chrome",
                "google chrome": "start chrome",
                "edge": "start msedge",
                "firefox": "start firefox",
                "notepad": "start notepad",
                "calculator": "start calc",
                "calc": "start calc",
                "word": "start winword",
                "excel": "start excel",
                "powerpoint": "start powerpnt",
                "paint": "start mspaint",
                "explorer": "start explorer",
                "file explorer": "start explorer",
                "settings": "start ms-settings:",
                "vlc": "start vlc",
                "spotify": "start spotify",
                "microsoft store": "start ms-windows-store:",
                "store": "start ms-windows-store:",
                "copilot": "start microsoft-edge://?ux=copilot",
                "ko pilot": "start microsoft-edge://?ux=copilot",
                "microsoft copilot": "start microsoft-edge://?ux=copilot"
            }
            
            # 1. Try direct launch first if it's a known application
            if app_name_lower in direct_launch_map:
                os.system(direct_launch_map[app_name_lower])
                time.sleep(1.0)
                return json.dumps({"status": "success", "action": f"Opening {app_name}"})
                
            # 2. Try generic start command (only for unknown apps to avoid Windows error popup)
            search_terms = {
                "whatsapp": "WhatsApp",
                "discord": "Discord",
                "telegram": "Telegram",
                "coconut": "Coconut"
            }
            
            if app_name_lower not in search_terms:
                try:
                    # Sometimes just 'start appname' works for Windows Store apps or PATH apps
                    # Redirect stderr so it doesn't pop up errors for command line
                    result = os.system(f"start {app_name_lower} 2>nul")
                except:
                    pass

            # 3. Fallback: Macro: Press Windows Key -> Type name -> Hit Enter
            # Map common names to what we should type in the search bar
            typing_term = search_terms.get(app_name_lower, app_name)
            
            pyautogui.press('win')
            time.sleep(0.8) # Wait for start menu to pop up
            pyautogui.write(typing_term, interval=0.05)
            time.sleep(1.5) # Wait for search results to populate
            pyautogui.press('enter')
            
            return json.dumps({"status": "success", "action": f"Opening {app_name}"})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Could not open {app_name}: {str(e)}"})

    def close_app(self, app_name: str) -> str:
        """Close an application or all applications."""
        try:
            app_name_lower = app_name.lower().strip()
            
            if app_name_lower == "all":
                # Close all user applications (but not critical system processes)
                safe_apps = [
                    "notepad.exe", "calc.exe", "wordpad.exe", "mspaint.exe",
                    "chrome.exe", "firefox.exe", "msedge.exe",
                    "winword.exe", "excel.exe", "powerpnt.exe",
                    "WhatsApp.exe", "Discord.exe", "Telegram.exe",
                    "vlc.exe", "spotify.exe"
                ]
                closed = 0
                for app in safe_apps:
                    try:
                        os.system(f"taskkill /IM {app} /F /T")
                        closed += 1
                    except:
                        pass
                
                return json.dumps({
                    "status": "success",
                    "message": f"Closed {closed} applications"
                })
            else:
                # Close specific application
                if app_name_lower in ["explorer", "file explorer"]:
                    try:
                        os.system('powershell -Command "(New-Object -comObject Shell.Application).Windows() | foreach-object {$_.quit()}"')
                        return json.dumps({"status": "success", "message": f"Closed File Explorer"})
                    except:
                        pass
                if app_name_lower == "browser":
                    os.system("taskkill /IM chrome.exe /F /T 2>nul")
                    os.system("taskkill /IM msedge.exe /F /T 2>nul")
                    os.system("taskkill /IM firefox.exe /F /T 2>nul")
                    return json.dumps({"status": "success", "message": "Closed browser"})

                # Web apps close the active tab instead of killing the browser
                if app_name_lower in ["gmail", "youtube", "facebook", "twitter", "instagram"]:
                    import pyautogui
                    pyautogui.hotkey('ctrl', 'w')
                    return json.dumps({"status": "success", "message": f"Closed tab for {app_name}"})
                    
                app_name_clean = app_name_lower.replace(" please", "").strip()

                if app_name_clean in ["tab", "this tab", "current tab"]:
                    return self.close_tab()
                    
                if app_name_clean in ["the app", "app", "it", "this", "window", "that", "current", "website", "the website"]:
                    import pyautogui
                    pyautogui.hotkey('alt', 'f4')
                    return json.dumps({"status": "success", "message": "Closed active window"})
                
                # WhatsApp often spawns aggressive web-view child processes
                if app_name_clean in ["whatsapp", "whatsapp web"]:
                    os.system('taskkill /IM WhatsApp.exe /F /T 2>nul')
                    # UWP WhatsApp might run as ApplicationFrameHost, but its MainWindowTitle is "WhatsApp"
                    # The PowerShell script below will catch it gracefully!

                app_map = {
                    "discord": "Discord.exe",
                    "telegram": "Telegram.exe",
                    "notepad": "notepad.exe",
                    "word": "winword.exe",
                    "excel": "excel.exe",
                    "powerpoint": "powerpnt.exe",
                    "outlook": "outlook.exe",
                    "calculator": "calc.exe",
                    "paint": "mspaint.exe",
                    "wordpad": "wordpad.exe",
                    "chrome": "chrome.exe",
                    "firefox": "firefox.exe",
                    "edge": "msedge.exe",
                    "ms edge": "msedge.exe",
                    "edge browser": "msedge.exe",
                    "vlc": "vlc.exe",
                    "photos": "Photos.exe",
                    "spotify": "spotify.exe",
                    "whatsapp": "WhatsApp.exe",
                    "settings": "SystemSettings.exe",
                    "file explorer": "explorer.exe",
                    "explorer": "explorer.exe"
                }
                
                if app_name_clean in app_map:
                    os.system(f"taskkill /IM {app_map[app_name_clean]} /F /T 2>nul")
                
                # Dynamic App / Website Closer using PowerShell
                # 1. Gracefully close Windows containing the name in their title
                # 2. Force kill exact process names or names stripped of spaces
                import subprocess
                ps_script = f"""
                $name = "{app_name_clean}"
                $nameNoSpace = $name -replace " ",""
                
                $windows = Get-Process | Where-Object {{ $_.MainWindowTitle -match "(?i).*$name.*" }}
                if ($windows) {{
                    $windows | ForEach-Object {{ $_.CloseMainWindow() | Out-Null }}
                    Start-Sleep -Milliseconds 500
                    $windows | Where-Object {{ -not $_.HasExited }} | Stop-Process -Force -ErrorAction SilentlyContinue
                }}
                
                Get-Process | Where-Object {{ $_.ProcessName -match "(?i)^$name$" -or $_.ProcessName -match "(?i)^$nameNoSpace$" }} | Stop-Process -Force -ErrorAction SilentlyContinue
                """
                
                try:
                    subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
                    return json.dumps({
                        "status": "success",
                        "message": f"Closed {app_name_clean}"
                    })
                except Exception as e:
                    return json.dumps({
                        "status": "error",
                        "message": f"Could not close {app_name}. {str(e)}"
                    })
                    
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Error closing app: {str(e)}"})


    def open_whatsapp_contact(self, recipient: str) -> str:
        """Open a specific WhatsApp contact's chat."""
        try:
            import pyautogui
            import time
            self.open_app("whatsapp")
            time.sleep(7.0) # Wait for it to fully load
            
            # Use Ctrl+F (Global Search)
            pyautogui.hotkey('ctrl', 'f') 
            time.sleep(1.0)
            
            # Type the contact name
            pyautogui.write(recipient, interval=0.05)
            time.sleep(3.0) # Wait for search results
            
            # Navigate to the first search result
            pyautogui.press('down')
            time.sleep(0.5)
            pyautogui.press('enter') # Select the chat
            
            return json.dumps({
                "status": "success",
                "message": f"Opened chat with {recipient}"
            })
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Error opening contact: {str(e)}"})

    def send_message(self, platform: str, recipient: str, message: str) -> str:
        """Send a message using keyboard automation."""
        try:
            import pyautogui
            import time
            platform = platform.lower().strip()
            
            if platform in ["whatsapp", "whatsapp web"]:
                # Open WhatsApp first
                self.open_app("whatsapp")
                time.sleep(7.0) # Wait for WhatsApp to fully open
                
                # Use Ctrl+F (Search)
                pyautogui.hotkey('ctrl', 'f') 
                time.sleep(1.0)
                
                # Type contact name
                pyautogui.write(recipient, interval=0.05)
                time.sleep(3.0) # Wait for search results
                
                # Press Down to enter the results list, then Enter
                pyautogui.press('down') 
                time.sleep(0.5)
                pyautogui.press('enter') # Select contact
                time.sleep(2.0) # Wait for conversation thread to open
                
                # Type message and send
                if message:
                    pyautogui.write(message, interval=0.05)
                    time.sleep(0.5)
                    pyautogui.press('enter')
                    return json.dumps({
                        "status": "success",
                        "message": f"Successfully sent WhatsApp message to {recipient}"
                    })
                else:
                    return json.dumps({
                        "status": "success",
                        "message": f"Opened chat with {recipient}"
                    })
            
            elif platform in ["gmail", "email"]:
                self.open_app("chrome")
                time.sleep(2.0)
                
                # Compose shortcut in Gmail (assumes Gmail is open, or we open it)
                webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1")
                time.sleep(3.0)
                
                # Type recipient
                pyautogui.write(recipient, interval=0.05)
                time.sleep(0.5)
                pyautogui.press('enter')
                pyautogui.press('tab') # Skip to subject
                pyautogui.write("Message from JARVIS")
                pyautogui.press('tab') # Skip to body
                
                # Type message
                if message:
                    pyautogui.write(message, interval=0.05)
                    time.sleep(0.5)
                    pyautogui.hotkey('ctrl', 'enter') # Send email
                    
                    return json.dumps({
                        "status": "success",
                        "message": f"Sent Email to {recipient}"
                    })
                else:
                    return json.dumps({
                        "status": "success",
                        "message": f"Opened Gmail draft to {recipient}"
                    })
            
            else:
                return json.dumps({"status": "error", "message": f"Unsupported platform: {platform}"})
                
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Error sending message: {str(e)}"})

    def open_website(self, url: str) -> str:
        """Open a website in the default browser."""
        try:
            url = url.lower().strip()
            
            # Map common site names to URLs
            site_map = {
                "google": "https://google.com",
                "youtube": "https://youtube.com",
                "youtube shorts": "https://youtube.com/shorts",
                "shorts": "https://youtube.com/shorts",
                "facebook": "https://facebook.com",
                "instagram": "https://instagram.com",
                "twitter": "https://twitter.com",
                "linkedin": "https://linkedin.com",
                "reddit": "https://reddit.com",
                "wikipedia": "https://wikipedia.org",
                "github": "https://github.com",
                "gmail": "https://mail.google.com"
            }
            
            # Add https if not present and no existing TLD is obvious
            if url in site_map:
                final_url = site_map[url]
            elif not url.startswith("http") and "." not in url:
                # If they say "open apple", search for apple instead of failing
                final_url = f"https://www.google.com/search?q={url.replace(' ', '+')}"
            elif not url.startswith("http"):
                final_url = f"https://{url}"
            else:
                final_url = url
            
            webbrowser.open(final_url)
            return json.dumps({"status": "success", "action": f"Opening {url.title()}"})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Error opening website: {str(e)}"})

    def take_screenshot(self) -> str:
        """Take a screenshot and save it."""
        try:
            import time
            filename = f"screenshot_{int(time.time())}.png"
            
            # Try using Screenshot tool in Windows
            os.system(f"snippingtool /clip")
            return json.dumps({"status": "success", "message": "Screenshot copied to clipboard"})
                
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Error taking screenshot: {str(e)}"})

    def search_and_play(self, query: str) -> str:
        """Search for and play a song or video on YouTube."""
        try:
            import yt_dlp
            
            # Search for the video using yt-dlp with ytsearch: prefix
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,  # Don't download, just extract info
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Use ytsearch1 to get just the first result
                info = ydl.extract_info(f'ytsearch1:{query}', download=False)
            
            if info and 'entries' in info and len(info['entries']) > 0:
                video_id = info['entries'][0].get('id')
                title = info['entries'][0].get('title', 'Unknown')
                
                if video_id:
                    # Open the direct YouTube link which will auto-play
                    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                    webbrowser.open(youtube_url)
                    
                    return json.dumps({
                        "status": "success",
                        "message": f"Playing '{title}' on YouTube"
                    })
            
            # Fallback to search results if no video found
            encoded_query = query.replace(" ", "+")
            youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            webbrowser.open(youtube_url)
            
            return json.dumps({
                "status": "success",
                "message": f"Opening YouTube search for '{query}'"
            })
            
        except Exception as e:
            # Fallback: open search results
            try:
                encoded_query = query.replace(" ", "+")
                youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
                webbrowser.open(youtube_url)
                
                return json.dumps({
                    "status": "success",
                    "message": f"Opening YouTube search for '{query}' (fallback)"
                })
            except:
                return json.dumps({
                    "status": "error",
                    "message": f"Error searching for '{query}'"
                })

    def _extract_phone_number(self, recipient: str) -> str:
        """Try to extract phone number from recipient string."""
        import re
        numbers = re.findall(r'\d+', recipient)
        if numbers:
            return "91" + numbers[-10:] if len(numbers[-1]) >= 10 else numbers[0]
        return ""
    def control_volume(self, action: str) -> str:
        """Control system/browser volume using keyboard shortcuts."""
        try:
            action_lower = action.lower().strip()
            
            # Import keyboard module for key control
            try:
                import pyautogui
                # Use pyautogui to send keyboard commands
                if "increase" in action_lower or "up" in action_lower:
                    # Increase volume
                    for _ in range(3):
                        pyautogui.press('volumeup')
                    return json.dumps({
                        "status": "success",
                        "message": "Volume increased"
                    })
                elif "decrease" in action_lower or "down" in action_lower:
                    # Decrease volume
                    for _ in range(3):
                        pyautogui.press('volumedown')
                    return json.dumps({
                        "status": "success",
                        "message": "Volume decreased"
                    })
                elif "mute" in action_lower:
                    # Mute volume
                    pyautogui.press('volumemute')
                    return json.dumps({
                        "status": "success",
                        "message": "Volume muted"
                    })
            except:
                # Fallback: use keyboard module if available
                try:
                    import keyboard
                    if "increase" in action_lower or "up" in action_lower:
                        keyboard.press_and_release('volume up')
                        return json.dumps({"status": "success", "message": "Volume increased"})
                    elif "decrease" in action_lower or "down" in action_lower:
                        keyboard.press_and_release('volume down')
                        return json.dumps({"status": "success", "message": "Volume decreased"})
                except:
                    pass
            
            return json.dumps({
                "status": "success",
                "message": f"Attempted to {action_lower} volume"
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error controlling volume: {str(e)}"
            })

    def pause_video(self) -> str:
        """Pause or stop the currently playing video using media key."""
        try:
            import pyautogui
            # Press playpause to pause/play video media
            pyautogui.press('playpause')
            return json.dumps({
                "status": "success",
                "message": "Video paused"
            })
        except:
            try:
                import keyboard
                keyboard.press_and_release('play/pause media')
                return json.dumps({
                    "status": "success",
                    "message": "Video paused"
                })
            except:
                return json.dumps({
                    "status": "success",
                    "message": "Pause command sent"
                })

    def close_tab(self) -> str:
        """Close the current browser tab using Ctrl+W."""
        try:
            import pyautogui
            # Press Ctrl+W to close current tab
            pyautogui.hotkey('ctrl', 'w')
            return json.dumps({
                "status": "success",
                "message": "Tab closed"
            })
        except:
            try:
                import keyboard
                keyboard.press_and_release('ctrl+w')
                return json.dumps({
                    "status": "success",
                    "message": "Tab closed"
                })
            except:
                # Fallback using os command
                os.system("taskkill /f /im chrome.exe")
                return json.dumps({
                    "status": "success",
                    "message": "Browser tab closed"
                })
    def app_control(self, command: str) -> str:
        """Unified app control: pause, play, volume, close, fullscreen, etc."""
        try:
            command_lower = command.lower().strip()
            
            try:
                import pyautogui
                
                if command_lower in ["pause", "stop"]:
                    pyautogui.press('playpause')
                    return json.dumps({"status": "success", "message": "Paused"})
                elif command_lower in ["play", "resume"]:
                    pyautogui.press('playpause')
                    return json.dumps({"status": "success", "message": "Playing"})
                elif command_lower == "volume_up":
                    pyautogui.press('volumeup')
                    return json.dumps({"status": "success", "message": "Volume increased"})
                elif command_lower == "volume_down":
                    pyautogui.press('volumedown')
                    return json.dumps({"status": "success", "message": "Volume decreased"})
                elif command_lower == "mute":
                    pyautogui.press('volumemute')
                    return json.dumps({"status": "success", "message": "Muted"})
                elif command_lower == "skip":
                    pyautogui.press('nexttrack')
                    return json.dumps({"status": "success", "message": "Skipped to next track"})
                elif command_lower == "forward":
                    pyautogui.press('l') # YouTube 10s forward
                    return json.dumps({"status": "success", "message": "Fast forwarded video"})
                elif command_lower == "rewind":
                    pyautogui.press('j') # YouTube 10s rewind
                    return json.dumps({"status": "success", "message": "Rewound video"})
                elif command_lower == "fullscreen":
                    pyautogui.press('f') # YouTube fullscreen is f, f11 is browser
                    return json.dumps({"status": "success", "message": "Toggled fullscreen"})
                elif command_lower in ["close", "exit"]:
                    pyautogui.hotkey('alt', 'f4')
                    return json.dumps({"status": "success", "message": "Closed application"})
                else:
                    return json.dumps({"status": "error", "message": f"Unknown command: {command}"})
            except ImportError:
                # Fallback if pyautogui not available
                try:
                    import keyboard
                    if command_lower == "pause":
                        keyboard.press_and_release('space')
                    elif command_lower == "mute":
                        keyboard.press_and_release('volume mute')
                    return json.dumps({"status": "success", "message": f"Executed {command}"})
                except:
                    return json.dumps({"status": "error", "message": "Could not execute command"})
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Error in app control: {str(e)}"})

    def keyboard_press(self, keys: str) -> str:
        """Press one or more keyboard keys."""
        try:
            import pyautogui
            keys_list = [k.strip().lower() for k in keys.split('+')]
            pyautogui.hotkey(*keys_list)
            return json.dumps({"status": "success", "message": f"Pressed {keys}"})
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Could not press {keys}: {str(e)}"})
            
    def keyboard_type(self, text: str) -> str:
        """Type the given text string."""
        try:
            import pyautogui
            pyautogui.write(text, interval=0.02)
            return json.dumps({"status": "success", "message": f"Typed text"})
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Could not type text: {str(e)}"})

    def mouse_control(self, action: str) -> str:
        """Control mouse actions."""
        try:
            import pyautogui
            action_lower = action.lower().strip()
            
            if action_lower == "left_click":
                pyautogui.click()
            elif action_lower == "right_click":
                pyautogui.rightClick()
            elif action_lower == "double_click":
                pyautogui.doubleClick()
            else:
                return json.dumps({"status": "error", "message": f"Unknown mouse action: {action}"})
                
            return json.dumps({"status": "success", "message": f"Performed {action}"})
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Could not perform mouse action: {str(e)}"})

    def youtube_control(self, action: str) -> str:
        """Control YouTube playback explicitly."""
        try:
            import pyautogui
            import time
            action_lower = action.lower().strip()
            
            if action_lower == "speed_up":
                pyautogui.hotkey('shift', '.')
                return json.dumps({"status": "success", "message": "Increased video speed"})
            elif action_lower == "speed_down":
                pyautogui.hotkey('shift', ',')
                return json.dumps({"status": "success", "message": "Decreased video speed"})
            elif action_lower == "normal_speed":
                # Ensure we reset to 1x by going all the way down and then up
                for _ in range(4):
                    pyautogui.hotkey('shift', ',')
                    time.sleep(0.1)
                for _ in range(3):
                    pyautogui.hotkey('shift', '.')
                    time.sleep(0.1)
                return json.dumps({"status": "success", "message": "Reset to normal speed"})
            elif action_lower == "volume_up":
                pyautogui.press('up')
                return json.dumps({"status": "success", "message": "Increased YouTube volume"})
            elif action_lower == "volume_down":
                pyautogui.press('down')
                return json.dumps({"status": "success", "message": "Decreased YouTube volume"})
            elif action_lower == "quality":
                return json.dumps({"status": "error", "message": "Quality control requires manual mouse interaction on YouTube. I cannot change quality via keyboard."})
            elif action_lower == "skip_ad":
                pyautogui.press('tab')
                pyautogui.press('enter')
                return json.dumps({"status": "success", "message": "Attempted to skip ad"})
            elif action_lower == "fullscreen":
                pyautogui.press('f')
                return json.dumps({"status": "success", "message": "Toggled fullscreen"})
            else:
                return json.dumps({"status": "error", "message": f"Unknown YouTube action: {action}"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def gmail_control(self, action: str) -> str:
        """Control Gmail via keyboard shortcuts."""
        try:
            import pyautogui
            import time
            action_lower = action.lower().strip()
            
            if action_lower == "compose":
                pyautogui.press('c')
                return json.dumps({"status": "success", "message": "Opened Gmail compose"})
            elif action_lower == "inbox":
                pyautogui.press('g')
                time.sleep(0.1)
                pyautogui.press('i')
                return json.dumps({"status": "success", "message": "Navigated to inbox"})
            elif action_lower == "unread":
                pyautogui.press('/')
                time.sleep(0.2)
                pyautogui.write("is:unread", interval=0.05)
                time.sleep(0.1)
                pyautogui.press('enter')
                return json.dumps({"status": "success", "message": "Searching for unread messages"})
            elif action_lower == "spam":
                pyautogui.press('/')
                time.sleep(0.2)
                pyautogui.write("in:spam", interval=0.05)
                time.sleep(0.1)
                pyautogui.press('enter')
                return json.dumps({"status": "success", "message": "Navigated to spam"})
            elif action_lower == "send":
                pyautogui.hotkey('ctrl', 'enter')
                return json.dumps({"status": "success", "message": "Sent email"})
            elif action_lower == "undo":
                pyautogui.press('z')
                return json.dumps({"status": "success", "message": "Undid last action"})
            elif action_lower == "redo":
                pyautogui.hotkey('ctrl', 'y')
                return json.dumps({"status": "success", "message": "Redid last action"})
            elif action_lower == "select_all":
                pyautogui.press('*')
                time.sleep(0.1)
                pyautogui.press('a')
                return json.dumps({"status": "success", "message": "Selected messages"})
            else:
                return json.dumps({"status": "error", "message": f"Unknown Gmail action: {action}"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def search_files(self, query: str) -> str:
        """Search for files in Windows natively."""
        try:
            import pyautogui
            import time
            pyautogui.press('win')
            time.sleep(0.8)
            pyautogui.write(query, interval=0.05)
            time.sleep(1.0)
            pyautogui.press('enter')
            return json.dumps({"status": "success", "message": f"Searched opening file explorer for {query}"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})