import random
from app.db import Base, engine, SessionLocal
from app.models import User, Chat
from app.security import hash_password
from faker import Faker

# Initialize Faker
fake = Faker('en_IN')  # Indian names/addresses

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Delete existing data (optional - comment out if you want to keep)
db.query(Chat).delete()
db.query(User).delete()
db.commit()

# Number of users to create
NUM_USERS = 200  # Change to 100 or 500 as needed
NUM_CHATS = 300  # Random chats between users

print(f"Creating {NUM_USERS} users...")

users = []
for i in range(NUM_USERS):
    first_name = fake.first_name()
    last_name = fake.last_name()
    full_name = f"{first_name} {last_name}"
    email = f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}"
    
    # Random batch (2024-2028)
    batch = str(random.randint(2024, 2028))
    
    # Random social_id (some blank)
    social_id = fake.url() if random.random() > 0.3 else ""
    
    user = User(
        full_name=full_name,
        email_id=email,
        social_id=social_id,
        batch=batch,
        pass_hash=hash_password("password123")  # Same password for all
    )
    users.append(user)
    if (i + 1) % 50 == 0:
        print(f"  Created {i + 1} users...")

db.add_all(users)
db.commit()
print(f"✅ {NUM_USERS} users created successfully!")

# Fetch user IDs
user_ids = [u.user_id for u in users]

print(f"Creating {NUM_CHATS} random chats...")
chats = []
for i in range(NUM_CHATS):
    # Pick two random different users
    user1, user2 = random.sample(user_ids, 2)
    
    messages = [
        "Hey! How's it going?",
        "Great to see you!",
        "Did you finish the assignment?",
        "Let's meet up later!",
        "Your presentation was amazing!",
        "Thanks for your help yesterday.",
        "Can we work on the project together?",
        "I really enjoyed our conversation.",
        "You're doing great work!",
        "Let's grab lunch sometime.",
        "What do you think about the new course?",
        "Happy to have you as a friend!",
        "I'm really impressed with your progress.",
        "Let me know if you need anything.",
        "You're the best!",
        "That was a fun event!",
        "Looking forward to our next meetup.",
        "I appreciate your support.",
        "You always have the best ideas.",
        "Let's collaborate on this project."
    ]
    
    chat = Chat(
        user_1_from=user1,
        user_2_to=user2,
        message=random.choice(messages)
    )
    chats.append(chat)

db.add_all(chats)
db.commit()
print(f"✅ {NUM_CHATS} chats created successfully!")

# Print summary
print("\n📊 Database Summary:")
print(f"  - Users: {db.query(User).count()}")
print(f"  - Chats: {db.query(Chat).count()}")

# Show sample users
print("\n📝 Sample users:")
for user in db.query(User).limit(5).all():
    print(f"  - {user.full_name} ({user.email_id})")

db.close()
print("\n✅ Database seeded successfully!")
print("🔑 Default password for all users: password123")