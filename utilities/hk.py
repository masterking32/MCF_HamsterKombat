import random
import string
import uuid


def DetectOS(user_agent):
    if "Android" in user_agent:
        return "Android"
    else:
        return "iOS"


def GenerateHKFingerprint(platform="iOS"):
    def random_float(start, end):
        return round(random.uniform(start, end), 7)

    def random_int(start, end):
        return random.randint(start, end)

    def random_fonts():
        ios_fonts = [
            "San Francisco",
            "Helvetica Neue",
            "Arial",
            "Courier",
            "Georgia",
            "Times New Roman",
            "Verdana",
            "Trebuchet MS",
            "Gill Sans",
            "Palatino",
            "Futura",
            "Marker Felt",
            "Chalkboard",
            "Chalkduster",
            "Hoefler Text",
            "Optima",
            "Baskerville",
            "American Typewriter",
            "Apple Color Emoji",
            "Apple Symbols",
            "Comic Sans MS",
            "Impact",
            "Lucida Grande",
            "Tahoma",
            "Geneva",
            "Copperplate",
            "Papyrus",
            "Brush Script MT",
            "Didot",
            "Garamond",
        ]

        android_fonts = [
            "Roboto",
            "Noto Sans",
            "Droid Sans",
            "Droid Serif",
            "Droid Sans Mono",
            "Roboto Condensed",
            "Roboto Slab",
            "Roboto Mono",
            "Noto Serif",
            "Noto Mono",
            "Cutive Mono",
            "Montserrat",
            "Lato",
            "Open Sans",
            "Merriweather",
            "Raleway",
            "Ubuntu",
            "PT Sans",
            "PT Serif",
            "Source Sans Pro",
            "Nunito",
            "Playfair Display",
            "Quicksand",
            "Rubik",
            "Titillium Web",
            "Zilla Slab",
            "Oswald",
            "Cabin",
            "Arvo",
            "Josefin Sans",
        ]

        if platform == "iOS":
            return random.sample(ios_fonts, random_int(2, 5))
        elif platform == "Android":
            return random.sample(android_fonts, random_int(2, 5))

    def random_timezone():
        timezones = [
            "Asia/Tehran",
            "America/New_York",
            "Europe/London",
            "Asia/Tokyo",
            "Africa/Cairo",
            "America/Los_Angeles",
            "America/Chicago",
            "America/Denver",
            "America/Phoenix",
            "America/Toronto",
            "America/Vancouver",
            "America/Mexico_City",
            "America/Sao_Paulo",
            "Europe/Paris",
            "Europe/Berlin",
            "Europe/Madrid",
            "Europe/Rome",
            "Europe/Moscow",
            "Asia/Shanghai",
            "Asia/Hong_Kong",
            "Asia/Singapore",
            "Asia/Kolkata",
            "Asia/Dubai",
            "Australia/Sydney",
            "Australia/Melbourne",
            "Australia/Brisbane",
            "Pacific/Auckland",
            "Pacific/Honolulu",
            "Africa/Johannesburg",
            "Africa/Lagos",
        ]
        return random.choice(timezones)

    def random_plugins():
        ios_plugins = [
            {
                "name": "QuickTime Plug-in",
                "description": "QuickTime Plug-in",
                "mimeTypes": [{"type": "video/quicktime", "suffixes": "mov,qt"}],
            },
            {
                "name": "iPhotoPhotocast",
                "description": "iPhotoPhotocast",
                "mimeTypes": [{"type": "application/photo", "suffixes": "photo"}],
            },
            {
                "name": "SharePoint Browser Plug-in",
                "description": "Microsoft Office",
                "mimeTypes": [
                    {"type": "application/x-sharepoint", "suffixes": "x-sharepoint"}
                ],
            },
            {
                "name": "Java Applet Plug-in",
                "description": "Java Applet Plug-in",
                "mimeTypes": [{"type": "application/x-java-applet", "suffixes": "jar"}],
            },
            {
                "name": "Shockwave Flash",
                "description": "Shockwave Flash",
                "mimeTypes": [
                    {"type": "application/x-shockwave-flash", "suffixes": "swf"}
                ],
            },
        ]

        android_plugins = [
            {
                "name": "Chrome PDF Viewer",
                "description": "Portable Document Format",
                "mimeTypes": [{"type": "application/pdf", "suffixes": "pdf"}],
            },
            {
                "name": "Widevine Content Decryption Module",
                "description": "Enables Widevine licenses for playback of HTML audio/video content",
                "mimeTypes": [
                    {"type": "application/x-ppapi-widevine-cdm", "suffixes": ""}
                ],
            },
            {
                "name": "Native Client",
                "description": "Enables the execution of native code within the browser",
                "mimeTypes": [{"type": "application/x-nacl", "suffixes": ""}],
            },
            {
                "name": "Shockwave Flash",
                "description": "Shockwave Flash",
                "mimeTypes": [
                    {"type": "application/x-shockwave-flash", "suffixes": "swf"}
                ],
            },
            {
                "name": "Chrome Remote Desktop Viewer",
                "description": "Enables remote access to your computer",
                "mimeTypes": [
                    {"type": "application/vnd.chromium.remoting-viewer", "suffixes": ""}
                ],
            },
        ]

        if platform == "iOS":
            return random.sample(ios_plugins, random_int(2, 5))
        elif platform == "Android":
            return random.sample(android_plugins, random_int(2, 5))

    def random_webgl_info():
        if platform == "iOS":
            return {
                "version": "WebGL 1.0 (OpenGL ES 2.0 Apple A7 GPU)",
                "vendor": "Apple Inc.",
                "vendorUnmasked": "Apple Inc.",
                "renderer": "Apple GPU",
                "rendererUnmasked": f"Apple A7 GPU",
                "shadingLanguageVersion": "WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Apple)",
            }
        elif platform == "Android":
            return {
                "version": "WebGL 1.0 (OpenGL ES 2.0 Chromium)",
                "vendor": "Google Inc.",
                "vendorUnmasked": "Google Inc.",
                "renderer": "WebKit WebGL",
                "rendererUnmasked": f"ANGLE (Qualcomm, Adreno {random_int(300, 700)} (0x00001E84) Direct3D11 vs_5_0 ps_5_0, D3D11)",
                "shadingLanguageVersion": "WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)",
            }

    data = {
        "initDataRaw": "",
        "fingerprint": {
            "version": "4.2.1",
            "visitorId": "".join(
                random.choices(string.ascii_letters + string.digits, k=32)
            ),
            "components": {
                "fonts": {"value": random_fonts(), "duration": random_int(10, 50)},
                "domBlockers": {"duration": random_int(1, 20)},
                "fontPreferences": {
                    "value": {
                        "default": random_float(100, 120),
                        "apple": random_float(100, 120),
                        "serif": random_float(100, 120),
                        "sans": random_float(100, 120),
                        "mono": random_float(90, 100),
                        "min": random_float(5, 10),
                        "system": random_float(110, 130),
                    },
                    "duration": random_int(1, 20),
                },
                "audio": {
                    "value": random_float(0.00001, 0.0001),
                    "duration": random_int(10, 30),
                },
                "screenFrame": {
                    "value": [0, 0, random_int(40, 60), 0],
                    "duration": random_int(1, 5),
                },
                "osCpu": {"duration": random_int(0, 5)},
                "languages": {"value": [["en-US"]], "duration": 0},
                "colorDepth": {"value": random.choice([24, 30, 32]), "duration": 0},
                "deviceMemory": {
                    "value": random.choice([4, 6, 8, 12, 16]),
                    "duration": 0,
                },
                "screenResolution": {
                    "value": [random_int(720, 2560), random_int(720, 2560)],
                    "duration": 0,
                },
                "hardwareConcurrency": {
                    "value": random.choice([4, 8, 16]),
                    "duration": 0,
                },
                "timezone": {"value": random_timezone(), "duration": 0},
                "sessionStorage": {
                    "value": random.choice([True, False]),
                    "duration": 0,
                },
                "localStorage": {"value": random.choice([True, False]), "duration": 0},
                "indexedDB": {"value": random.choice([True, False]), "duration": 0},
                "openDatabase": {"value": random.choice([True, False]), "duration": 0},
                "cpuClass": {"duration": 0},
                "platform": {"value": platform, "duration": 0},
                "plugins": {"value": random_plugins(), "duration": random_int(1, 20)},
                "touchSupport": {
                    "value": {
                        "maxTouchPoints": random_int(0, 10),
                        "touchEvent": random.choice([True, False]),
                        "touchStart": random.choice([True, False]),
                    },
                    "duration": 0,
                },
                "vendor": {
                    "value": "Apple Inc." if platform == "iOS" else "Google Inc.",
                    "duration": 0,
                },
                "vendorFlavors": {
                    "value": ["safari"] if platform == "iOS" else ["chrome"],
                    "duration": 0,
                },
                "cookiesEnabled": {
                    "value": random.choice([True, False]),
                    "duration": 0,
                },
                "colorGamut": {"value": random.choice(["srgb", "p3"]), "duration": 0},
                "invertedColors": {"duration": random_int(0, 5)},
                "forcedColors": {"value": False, "duration": 0},
                "monochrome": {"value": random_int(0, 1), "duration": 0},
                "contrast": {"value": random_int(0, 5), "duration": 0},
                "webGlBasics": {
                    "value": random_webgl_info(),
                    "duration": random_int(1, 10),
                },
            },
        },
    }

    return data
