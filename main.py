from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import re

# === ORM konfiguratsiyasi ===
Base = declarative_base()
engine = create_engine("sqlite:///users.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# === User modeli ===
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
    birthdate = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    job = Column(String, nullable=True)
    password = Column(String, nullable=False)


# === Foydalanuvchini ro‘yxatdan o‘tkazish ===
def password_strength(password):
    import string
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    length = len(password)
    if length < 6:
        return "Oson"
    elif has_digit and (has_upper or has_lower):
        if has_symbol and length >= 8:
            return "Kuchli"
        return "O‘rtacha"
    return "Oson"

def register():
    print("\n📝 Ro‘yxatdan o‘tish")
    username = input("👤 Username: ")

    while True:
        email = input("📧 Email: ")
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
            break
        else:
            print("❌ Email noto‘g‘ri!")

    while True:
        phone = input("📱 Telefon raqam (+998901234567): ")
        if re.match(r"^\+998\d{9}$", phone):
            break
        else:
            print("❌ Telefon noto‘g‘ri!")

    address = input("🏠 Yashash manzil: ")
    birthdate = input("🎂 Tug‘ilgan sana (YYYY-MM-DD): ")
    
    while True:
        gender = input("👫 Jins (Erkak/Ayol): ").lower()
        if gender in ["erkak", "ayol"]:
            break
        else:
            print("❌ Faqat 'Erkak' yoki 'Ayol' kiriting!")

    job = input("💼 Kasbingiz: ")

    while True:
        password = input("🔒 Parol: ")
        strength = password_strength(password)
        print(f"🧠 Parol kuchi: {strength}")
        if strength == "Oson":
            print("❗ Parol juda oson! Iltimos kuchliroq parol kiriting.")
        else:
            break

    if session.query(User).filter((User.username == username) | (User.email == email)).first():
        print("❌ Username yoki email band!")
        return

    user = User(
        username=username,
        email=email,
        phone=phone,
        address=address,
        birthdate=birthdate,
        gender=gender.capitalize(),
        job=job,
        password=password
    )
    session.add(user)
    session.commit()
    print("✅ Ro‘yxatdan o‘tildi!")



# === Kirish ===
def login():
    print("\n🔐 Tizimga kirish")
    username = input("👤 Username: ")
    password = input("🔑 Parol: ")

    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        print(f"✅ Xush kelibsiz, {username}!")
    else:
        print("❌ Noto‘g‘ri login yoki parol!")

# === Foydalanuvchini o‘chirish ===
def delete_user():
    print("\n🗑️ Foydalanuvchini o‘chirish")
    username = input("👤 Username: ")
    password = input("🔑 Parol: ")

    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        session.delete(user)
        session.commit()
        print("✅ Foydalanuvchi o‘chirildi.")
    else:
        print("❌ Topilmadi yoki parol noto‘g‘ri!")

# === Admin panel ===
def admin_panel():
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"
    print("\n🔐 Admin panel")

    for _ in range(3):
        username = input("👤 Admin username: ")
        password = input("🔑 Admin parol: ")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            break
        else:
            print("❌ Noto‘g‘ri!")
    else:
        print("🚫 3 marta noto‘g‘ri urinish.")
        return

    while True:
        print("\n1. 👥 Barcha foydalanuvchilar")
        print("2. 🗑️ Foydalanuvchini o‘chirish")
        print("3. ✏️ Ma'lumotni tahrirlash")
        print("0. 🚪 Chiqish")

        tanlov = input("Tanlang: ")

        if tanlov == "1":
            users = session.query(User).all()
            for u in users:
                print(f"{u.username} | {u.email} | {u.phone}")
        elif tanlov == "2":
            uname = input("Username: ")
            user = session.query(User).filter_by(username=uname).first()
            if user:
                session.delete(user)
                session.commit()
                print("✅ O‘chirildi.")
            else:
                print("❌ Topilmadi.")
        elif tanlov == "3":
            uname = input("Tahrirlanadigan username: ")
            user = session.query(User).filter_by(username=uname).first()
            if user:
                print("1. Username\n2. Email\n3. Phone\n4. Parol\n0. Ortga")
                sub = input("Tanlang: ")
                if sub == "1":
                    user.username = input("Yangi username: ")
                elif sub == "2":
                    user.email = input("Yangi email: ")
                elif sub == "3":
                    user.phone = input("Yangi telefon: ")
                elif sub == "4":
                    user.password = input("Yangi parol: ")
                elif sub == "0":
                    continue
                else:
                    print("❌ Noto‘g‘ri tanlov.")
                    continue
                session.commit()
                print("✅ Yangilandi!")
            else:
                print("❌ Topilmadi.")
        elif tanlov == "0":
            break
        else:
            print("❌ Noto‘g‘ri tanlov.")

# === Menyu ===
def menu():
    Base.metadata.create_all(bind=engine)

    while True:
        print("\n📋 MENYU")
        print("1. 📝 Ro‘yxatdan o‘tish")
        print("2. 🔐 Kirish")
        print("3. 🗑️ O‘chirish")
        print("4. 🛠️ Admin panel")
        print("0. 🚪 Chiqish")

        tanlov = input("Tanlang: ")

        if tanlov == "1":
            register()
        elif tanlov == "2":
            login()
        elif tanlov == "3":
            delete_user()
        elif tanlov == "4":
            admin_panel()
        elif tanlov == "0":
            print("👋 Chiqildi.")
            break
        else:
            print("❌ Noto‘g‘ri tanlov.")

# === Ishga tushurish ===
if __name__ == "__main__":
    menu()
