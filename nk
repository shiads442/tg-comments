    try:
        data = json.loads(post_data.decode('utf-8'))
        text = data.get('text', '')
        user = data.get('user', {})
        
        user_id = user.get('id', 0)
        first_name = user.get('first_name', 'Невідомий')
        username = user.get('username', 'немає')
        
        TOKEN = os.environ.get('BOT_TOKEN')
        ADMIN_ID = os.environ.get('ADMIN_ID')
        
        if not TOKEN or not ADMIN_ID:
            raise Exception("Missing environment variables")
        
        msg = (
            f"Новий приватний коментар!\n\n"
            f"Від: {first_name} (@{username}, ID: {user_id})\n"
            f"Текст:\n{text}"
        )
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = json.dumps({
            "chat_id": ADMIN_ID,
            "text": msg,
            "parse_mode": "HTML"
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            response.read()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode('utf-8'))
        
    except Exception as e:
        self.send_response(500)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode('utf-8'))
