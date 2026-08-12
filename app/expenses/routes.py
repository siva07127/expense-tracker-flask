from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import func

from app import db
from app.models import Expense

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please login first.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapper

@expenses_bp.route("/")
@login_required
def index():
    user_id = session["user_id"]

    expenses = (
        Expense.query
        .filter_by(user_id=user_id)
        .order_by(Expense.expense_date.desc(), Expense.id.desc())
        .all()
    )

    total = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == user_id)
        .scalar()
    )

    categories = {}
    for expense in expenses:
        categories[expense.category] = categories.get(expense.category, 0) + expense.amount

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=categories
    )

@expenses_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount_text = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date_text = request.form.get("expense_date", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not amount_text or not category or not expense_date_text:
            flash("Please fill all required fields.", "danger")
            return render_template("add.html")

        try:
            amount = float(amount_text)
            expense_date = datetime.strptime(expense_date_text, "%Y-%m-%d").date()

            if amount < 0:
                raise ValueError
        except ValueError:
            flash("Enter a valid amount and date.", "danger")
            return render_template("add.html")

        expense = Expense(
            title=title,
            amount=amount,
            category=category,
            expense_date=expense_date,
            description=description,
            user_id=session["user_id"]
        )

        db.session.add(expense)
        db.session.commit()

        flash("Expense added successfully!", "success")
        return redirect(url_for("expenses.index"))

    return render_template("add.html")

@expenses_bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_expense(id):
    expense = Expense.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first()

    if expense is None:
        flash("Expense not found.", "danger")
        return redirect(url_for("expenses.index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount_text = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date_text = request.form.get("expense_date", "").strip()
        description = request.form.get("description", "").strip()

        try:
            amount = float(amount_text)
            expense_date = datetime.strptime(expense_date_text, "%Y-%m-%d").date()

            if amount < 0:
                raise ValueError

            if not title or not category:
                raise ValueError
        except ValueError:
            flash("Please enter valid expense details.", "danger")
            return render_template("update.html", expense=expense)

        expense.title = title
        expense.amount = amount
        expense.category = category
        expense.expense_date = expense_date
        expense.description = description

        db.session.commit()

        flash("Expense updated successfully!", "success")
        return redirect(url_for("expenses.index"))

    return render_template("update.html", expense=expense)

@expenses_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_expense(id):
    expense = Expense.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first()

    if expense is None:
        flash("Expense not found.", "danger")
        return redirect(url_for("expenses.index"))

    db.session.delete(expense)
    db.session.commit()

    flash("Expense deleted successfully!", "success")
    return redirect(url_for("expenses.index"))
