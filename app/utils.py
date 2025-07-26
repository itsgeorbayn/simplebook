import re, string, random, uuid, os, smtplib, sys, requests
from datetime import timedelta
from flask import flash, redirect, url_for, request, jsonify
from flask_login import current_user
from functools import wraps
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list) or isinstance(item, tuple):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def to_sentence_case(s):
    s = s.split()[-1]
    result = (s[:1].upper() + s[1:] if s else '').replace('_', ' ')
    return result

def is_email_or_username(field):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", field):
        return "email"
    return "username"

def generate_random_text(size):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=size))

def trim_symbols(s):
    return re.sub(" +", " ", s)

def require_not_banned(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_banned:
            flash("You can't do this due to your ban!", "error")
            return redirect(url_for('profile.profile'))
        return func(*args, **kwargs)
    return wrapper

def format_short_delta(delta: timedelta) -> str:
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours}h"
    else:
        days = seconds // 86400
        return f"{days}d"

def check_verify_status():
    if not current_user.is_verified:
        flash("Verify before you can do this", 'warning')
        
        return redirect(url_for('auth.verification_form'))

def translate_checkbox(value):
    return True if value == "on" else False

class Symbols:
    """
    Represents symbol lists, that can be useful in your code
    """
    
    allowed_symbols = list("abcdefghijklmnopqrstuvwxyzабвгґдеєжзиіїйклмнопрстуфхцчшщьюя0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГ?ДЕЄЖЗИ?ЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯu!\"#$%&'()*+./:;<=>?@[\\]^_`{|}~")

    @classmethod
    def slug(cls):
        return uuid.uuid4().hex[:16]
    
    @classmethod
    def clean_title(cls, title):
        pattern = '[^' + re.escape(''.join(Symbols.allowed_symbols)) + ']'
        return trim_symbols(re.sub(pattern, ' ', title)).strip()

def count_lines():
    base_path = 'app/models'

    extensions = ('.py')
    total_lines = 0
    file_stats = []

    if not os.path.isdir(base_path):
        print(f"The specified path does not exist: {base_path}")
    else:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(extensions):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            line_count = len(lines)
                            total_lines += line_count
                            file_stats.append((path, line_count))
                    except Exception as e:
                        print(f"Error while reading {path}: {e}")

        for path, count in sorted(file_stats):
            print(f"{path}: {count} строк")

        print(f"\nTotal number of lines in .py and .html files: {total_lines}")
        
def bool_conv(val: str):
    val = val.lower()
    if val.lower() == "true":
        return True
    elif val.lower() == "false":
        return False
    else:
        return None
    
def fix_img_src_paths(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src.startswith('../static/'):
            img['src'] = src.replace('../static/', '/static/')
            
    return str(soup)

def send_email(subject, body, recipient):
    msg = MIMEText(body)
    
    msg['Subject'] = subject
    msg['From'] = 'georgebaynak860@gmail.com'
    msg['To'] = recipient
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login('georgebaynak860@gmail.com', Config.APP_PASSWORD)
        smtp_server.sendmail('georgebaynak860@gmail.com', recipient, msg.as_string())
    
    return True

def upload_to_supabase(file, bucket_name, another_name=None, subdir="users"):
    headers = {
        "apikey": os.environ.get("SUPABASE_KEY"),
        "Authorization": f"Bearer {os.environ.get('SUPABASE_KEY')}",
        "Content-Type": file.content_type,
        "x-upsert": "true"
    }
    
    filename = another_name if another_name else file.filename
    storage_path = f"{subdir}/{filename}"
    url = f"{os.environ.get('SUPABASE_URL')}/storage/v1/object/{bucket_name}/{storage_path}"
    
    response = requests.post(url, headers=headers, data=file.read())

    if response.status_code == 200:
        public_url = f"{os.environ.get('SUPABASE_URL')}/storage/v1/object/public/{bucket_name}/{storage_path}"
        return {"success": True, "url": public_url}
    else:
        return {"success": False, "error": response.text}
    
    
def delete_from_supabase(bucket_name, file_path):
    headers = {
        "apikey": os.environ.get("SUPABASE_KEY"),
        "Authorization": f"Bearer {os.environ.get('SUPABASE_KEY')}",
    }
    
    url = f"{os.environ.get('SUPABASE_URL')}/storage/v1/object/{bucket_name}/{file_path}"
    
    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        return {"success": True}
    else:
        return {"success": False, "error": response.text}