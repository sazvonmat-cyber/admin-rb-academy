import os, json, time, random, datetime
from flask import Flask, request, jsonify, send_file, Response
from groq import Groq

client = Groq(api_key='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', timeout=25.0)
app = Flask(__name__)
DB_PATH = "/data/academy_v3.json" if os.path.exists("/data") else r"D:\Admin_Academy\academy_v3.json"

ROLE_DAYS = {"Хелпер (Helper)": 7, "Младший Модератор": 14, "Старший Модератор": 21, "Администратор": 30, "Старший Администратор": 30, "Куратор Проекта": 30}

LESSONS = [
    {"id": "cmd", "day": 1, "title": "⌨️ Модуль 1: Справочник команд РБ и строгие запреты", "short": "Синтаксис команд модерации, сроки наказаний и запрещённые права.",
     "text": "<h3>1. Базовые команды и сетка наказаний</h3><ul><li><code>/warn [ник] [причина]</code> — предупреждение за лёгкий флуд или капс (3 варна = автомут).</li><li><code>/mute [ник] [время] [причина]</code> — мут чата: 15m (флуд), 1h (оскорбления), 12h (розжиг), 24h (реклама).</li><li><code>/kick [ник] [причина]</code> — отключение от сессии за помеху на спавне.</li></ul><h3>2. Команды проверки и блокировки</h3><ul><li><code>/spec [ник]</code> — скрытое наблюдение за игроком.</li><li><code>/freeze [ник]</code> — заморозка передвижения для проверки.</li><li><code>/ban [ник] [срок] [причина]</code> — блокировка аккаунта (за читы и скам — навсегда <code>perm</code>).</li></ul><h3 style='color:#f87171;'>3. ЗАПРЕЩЁННЫЕ КОМАНДЫ (Снятие + ЧС)</h3><p>Запрещено выдавать игрокам или использовать в личных целях: <code>/op</code>, <code>/setrank</code>, <code>/give</code>, <code>/eco</code>, <code>/fly</code>, <code>/god</code>, <code>/tpall</code>.</p>"},
    {"id": "cheat", "day": 2, "title": "🛡️ Модуль 2: Античит — SpeedHack, FlyHack, Noclip и пинг", "short": "Как отличать читы от лагов и оформлять видеодоказательства.",
     "text": "<h3>Пинг против реальных читов</h3><ul><li><b>Высокий пинг:</b> игрок замирает на 1–3 сек, затем телепортируется и бежит с обычной скоростью.</li><li><b>SpeedHack:</b> плавный бег в 3–5 раз быстрее нормы без баффов.</li><li><b>FlyHack:</b> парение в воздухе вне платформ дольше 3 секунд.</li><li><b>Noclip:</b> проход сквозь закрытые двери и стены.</li></ul><h3>Алгоритм действий</h3><p>Включите <code>/spec [ник]</code>, запишите минимум 10–15 секунд видео с видимым ником и выдайте <code>/ban perm</code>.</p>"},
    {"id": "scam", "day": 3, "title": "🔒 Модуль 3: Защита от скама, фишинга и фейк-админов", "short": "Пресечение кражи аккаунтов Roblox и обмана в трейдах.",
     "text": "<h3>Схемы обмана</h3><ul><li><b>Фейк-админы:</b> меняют буквы в нике (<code>l</code> на <code>I</code>) и требуют пароль от аккаунта. Настоящая администрация никогда не спрашивает пароли.</li><li><b>Фишинг:</b> ссылки на сайты бесплатных робуксов.</li></ul><p><b>Наказание:</b> Немедленный <code>/banip perm</code> и очистка чата <code>/clearchat</code>.</p>"},
    {"id": "ethic", "day": 4, "title": "⚖️ Модуль 4: Этика администрации и запрет на блат", "short": "Поведение при провокациях и работа с жалобами.",
     "text": "<h3>Правила поведения</h3><p>Сохраняйте хладнокровие при провокациях, не отвечайте матом. Запрещено размучивать друзей без доказательств ошибки или торговать правами за игровую валюту.</p>"}
]

def get_mods(role):
    max_d = ROLE_DAYS.get(role, 7)
    res = [m for m in LESSONS if m["day"] <= max_d]
    for d in range(5, max_d + 1):
        res.append({"id": f"day_{d}", "day": d, "title": f"📅 Модуль {d} (День {d}/{max_d}): Практикум", "short": f"Сложные кейсы дня {d} ({role}).",
                    "text": f"<h3>Практикум — День {d}</h3><ul><li><b>Проверка дюпа:</b> при резком приросте валюты заморозьте аккаунт (<code>/freeze</code>) и передайте логи Старшему Админу.</li><li><b>Рейд спам-ботов:</b> включите <code>/slowmode 10</code>.</li></ul>"})
    return res

def load_db():
    if os.path.exists(DB_PATH):
        try: return json.load(open(DB_PATH, "r", encoding="utf-8"))
        except Exception: pass
    return {}

def save_db(db):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    json.dump(db, open(DB_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

DB = load_db()

@app.route("/")
def index(): return send_file("index.html")

@app.route("/googlebf13c19317e00fa1.html")
def google_verify():
    return Response("google-site-verification: googlebf13c19317e00fa1.html", mimetype="text/html")

@app.route("/robots.txt")
def robots(): return Response("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n", mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap():
    host = request.host_url.rstrip("/")
    return Response(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://sitemaps.org"><url><loc>{host}/</loc><priority>1.0</priority></url></urlset>', mimetype="application/xml")

@app.route("/api/candidates")
def get_cands():
    res = [{"user": u, "rbx": i.get("rbx", ""), "role": i["role"], "score": i["best_score"], "cert_id": i["cert_id"], "verdict": i.get("verdict", "")} for u, i in DB.items() if i.get("best_score", 0) > 0]
    res.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(res)

@app.route("/api/save_rbx", methods=["POST"])
def save_rbx():
    d = request.json or {}; user = str(d.get("user", "")); rbx = str(d.get("rbx", "")).strip()
    if user not in DB or not rbx: return jsonify({"ok": False})
    DB[user]["rbx"] = rbx
    save_db(DB)
    return jsonify({"ok": True, "rbx": rbx})

@app.route("/api/promote", methods=["POST"])
def promote():
    d = request.json or {}; user = str(d.get("user", "")); new_role = str(d.get("new_role", ""))
    if user not in DB or new_role not in ROLE_DAYS: return jsonify({"ok": False, "msg": "Ошибка выбора должности!"})
    p = DB[user]
    if p["role"] == new_role: return jsonify({"ok": False, "msg": "Вы уже на этой должности!"})
    hist = p.setdefault("history", [])
    if p.get("best_score", 0) > 0:
        hist.append(f"{p['role']} ({p['best_score']}/100)")
    p["role"] = new_role; p["tests"] = {}; p["best_score"] = 0
    p, mods = prep(user)
    p["verdict"] = f"Кандидат {user} начал курс на должность «{new_role}»."
    save_db(DB)
    return jsonify({"ok": True, "profile": p, "modules": mods})

def prep(user):
    p = DB[user]; mods = get_mods(p["role"]); chain = 0
    for m in mods:
        t = p["tests"].get(m["id"], {})
        if t.get("best", 0) >= 75 or t.get("attempts", 0) >= 3: chain += 1
        else: break
    total_mods = len(mods)
    p["unlocked_day"] = min(total_mods, chain + 1); p["max_days"] = total_mods; p["passed_count"] = chain
    return p, mods

@app.route("/api/auth", methods=["POST"])
def auth():
    d = request.json or {}; mode = d.get("mode", "login")
    user = str(d.get("user", "")).strip(); pwd = str(d.get("pass", "")).strip(); role = str(d.get("role", "Хелпер (Helper)"))
    if not user or not pwd: return jsonify({"ok": False, "msg": "Заполните никнейм и пароль!"})
    ex = next((k for k in DB if k.lower() == user.lower()), None)
    if mode == "reg":
        if ex: return jsonify({"ok": False, "msg": f"Имя «{ex}» уже занято! Придумайте другой ник."})
        DB[user] = {"pass": pwd, "role": role, "tests": {}, "best_score": 0, "cert_id": f"PRO-{random.randint(10000,99999)}", "verdict": ""}
    else:
        if not ex: return jsonify({"ok": False, "msg": "Аккаунт не найден!"})
        if DB[ex]["pass"] != pwd: return jsonify({"ok": False, "msg": "Неверный пароль!"})
        user = ex
    p, mods = prep(user); save_db(DB)
    return jsonify({"ok": True, "user": user, "profile": p, "modules": mods})

@app.route("/api/get_quiz", methods=["POST"])
def get_quiz():
    d = request.json or {}; user = str(d.get("user", "")); mid = str(d.get("mod_id", "cmd")); role = str(d.get("role", "Хелпер (Helper)"))
    if user in DB:
        t = DB[user]["tests"].get(mid, {})
        if t.get("attempts", 0) >= 3: return jsonify({"ok": False, "msg": "Все 3 попытки использованы!"})
        if t.get("cooldown_until", 0) > time.time():
            rem = int(t["cooldown_until"] - time.time())
            return jsonify({"ok": False, "msg": f"Повторная попытка через {rem // 60} мин {rem % 60} сек."})
    mods = get_mods(role); mod = next((m for m in mods if m["id"] == mid), mods.pop(0))
    try:
        sys_p = f'Ты строгий экзаменатор. Составь тест (билет #{random.randint(100,9999)}) из 4 сложных вопросов СТРОГО ПО ТЕКСТУ ЭТОЙ ЛЕКЦИИ и ни шагу в сторону: {mod["text"]}. Запрещено придумывать команды, которых нет в тексте лекции! Используй только команды и правила из текста выше. Верни ТОЛЬКО JSON: {{"questions": [{{"q": "Вопрос по тексту лекции", "opts": ["Вариант А", "Вариант Б", "Вариант В"], "ans": 0}}]}}'
        r = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role": "system", "content": sys_p}], temperature=0.9, max_tokens=750)
        raw = r.choices.pop(0).message.content or "{}"
        qs = json.loads(raw[raw.find("{"):raw.rfind("}")+1])["questions"]
    except Exception:
        qs = [
            {"q": "Игрок замер на 2 сек, а затем телепортировался вперёд и бежит нормально. Ваши действия?", "opts": ["Не банить: это лаги (пинг), а не читы", "Сразу выдать /ban perm", "Выдать /op"], "ans": 0},
            {"q": "Игрок просит пароль в ЛС от имени помощника создателя. Наказание?", "opts": ["Немедленный /banip perm за попытку взлома", "Выдать /warn", "Мут 15 минут"], "ans": 0},
            {"q": "Минимум секунд видеофиксации читера перед баном?", "opts": ["10–15 секунд с видимым ником", "1 скриншот", "Видео не нужно"], "ans": 0},
            {"q": "Игрок предлагает предмет за снятие мута другу. Ваши действия?", "opts": ["Отказать: блат и торговля правами запрещены", "Снять мут", "Выдать себе предмет"], "ans": 0}
        ]
    return jsonify({"ok": True, "questions": qs})

@app.route("/api/submit_quiz", methods=["POST"])
def submit_quiz():
    d = request.json or {}; user = str(d.get("user", "")); mid = str(d.get("mod_id", "")); score = int(d.get("score", 0)); ch = bool(d.get("cheated", False))
    if user not in DB: return jsonify({"ok": False})
    p = DB[user]; t = p["tests"].get(mid, {"attempts": 0, "best": 0, "cooldown_until": 0}); now = time.time()
    if t.get("cooldown_until", 0) > now and not ch: return jsonify({"ok": False, "msg": "Ожидайте 15 минут!"})
    if ch: score = 0
    t["attempts"] += 1
    if score > t["best"]: t["best"] = score
    passed = score >= 75
    t["cooldown_until"] = (now + 900) if (not passed and t["attempts"] < 3) else 0
    p["tests"][mid] = t
    bests = [v["best"] for v in p["tests"].values()]
    p["best_score"] = round(sum(bests) / max(1, len(bests)))
    p, mods = prep(user)
    p["verdict"] = f"Кандидат {user} прошёл {p['passed_count']}/{p['max_days']} модулей на «{p['role']}» (лучший балл: {p['best_score']}/100)."
    save_db(DB)
    return jsonify({"ok": True, "passed": passed, "t_info": t, "profile": p, "modules": mods})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
