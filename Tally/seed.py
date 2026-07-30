from datetime import datetime, timedelta, timezone
from app.database import SessionLocal
from app import models
from app.core.security import get_password_hash

def seed_rich_data():
    db = SessionLocal()
    try:
        print("🌱 Seeding advanced test data...")

        # 1. Clean existing records safely
        db.query(models.ExpenseSplit).delete()
        db.query(models.Expense).delete()
        db.query(models.GroupMember).delete()
        db.query(models.ExpenseGroup).delete()
        db.query(models.User).delete()
        db.commit()

        # 2. Create Users
        pw = get_password_hash("password123")
        u1 = models.User(name="Areeba", email="areeba@example.com", hashed_password=pw)
        u2 = models.User(name="Ali", email="ali@example.com", hashed_password=pw)
        u3 = models.User(name="Sara", email="sara@example.com", hashed_password=pw)
        u4 = models.User(name="Zain", email="zain@example.com", hashed_password=pw) # Extra user who might not pay for things
        
        db.add_all([u1, u2, u3, u4])
        db.commit()
        for u in [u1, u2, u3, u4]: db.refresh(u)
        print("✅ Created 4 users (Areeba, Ali, Sara, Zain)")

        # 3. Create Groups
        g1 = models.ExpenseGroup(name="Lahore Trip", created_by=u1.id)
        g2 = models.ExpenseGroup(name="Apartment Rent", created_by=u2.id)
        db.add_all([g1, g2])
        db.commit()
        db.refresh(g1)
        db.refresh(g2)
        print("✅ Created 2 groups: 'Lahore Trip' and 'Apartment Rent'")

        # 4. Add Group Members
        # Goa Trip: Areeba, Ali, Sara
        db.add_all([
            models.GroupMember(group_id=g1.id, user_id=u1.id),
            models.GroupMember(group_id=g1.id, user_id=u2.id),
            models.GroupMember(group_id=g1.id, user_id=u3.id),
        ])
        # Apartment Rent: Ali, Sara, Zain (Areeba is not in this one)
        db.add_all([
            models.GroupMember(group_id=g2.id, user_id=u2.id),
            models.GroupMember(group_id=g2.id, user_id=u3.id),
            models.GroupMember(group_id=g2.id, user_id=u4.id),
        ])
        db.commit()
        print("✅ Added members to groups")

        # 5. Create Expenses & Splits for Group 1 (Goa Trip)
        # Expense A: Areeba pays 6000 cents ($60) for Food, split equally (2000 each)
        exp1 = models.Expense(
            group_id=g1.id, description="Beachside Dinner", amount_cents=6000, category="Food", paid_by=u1.id,
            created_at=datetime.now(timezone.utc) - timedelta(days=5)
        )
        db.add(exp1); db.commit(); db.refresh(exp1)
        db.add_all([
            models.ExpenseSplit(expense_id=exp1.id, user_id=u1.id, share_cents=2000),
            models.ExpenseSplit(expense_id=exp1.id, user_id=u2.id, share_cents=2000),
            models.ExpenseSplit(expense_id=exp1.id, user_id=u3.id, share_cents=2000),
        ])

        # Expense B: Ali pays 12000 cents ($120) for Travel/Hotel, split equally (4000 each)
        exp2 = models.Expense(
            group_id=g1.id, description="Hotel Booking", amount_cents=12000, category="Travel", paid_by=u2.id,
            created_at=datetime.now(timezone.utc) - timedelta(days=3)
        )
        db.add(exp2); db.commit(); db.refresh(exp2)
        db.add_all([
            models.ExpenseSplit(expense_id=exp2.id, user_id=u1.id, share_cents=4000),
            models.ExpenseSplit(expense_id=exp2.id, user_id=u2.id, share_cents=4000),
            models.ExpenseSplit(expense_id=exp2.id, user_id=u3.id, share_cents=4000),
        ])

        # Expense C: Sara pays 3000 cents ($30) for Groceries, uneven split (Areeba: 1000, Ali: 1500, Sara: 500)
        exp3 = models.Expense(
            group_id=g1.id, description="Supermarket run", amount_cents=3000, category="Groceries", paid_by=u3.id,
            created_at=datetime.now(timezone.utc) - timedelta(days=1)
        )
        db.add(exp3); db.commit(); db.refresh(exp3)
        db.add_all([
            models.ExpenseSplit(expense_id=exp3.id, user_id=u1.id, share_cents=1000),
            models.ExpenseSplit(expense_id=exp3.id, user_id=u2.id, share_cents=1500),
            models.ExpenseSplit(expense_id=exp3.id, user_id=u3.id, share_cents=500),
        ])

        db.commit()
        print("✅ Created diverse expenses and splits for 'Goa Trip'")
        print("🎉 Advanced database seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_rich_data()