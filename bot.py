import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
        CommandHandler,
            ContextTypes,
            )

            # ==============================
            # CONFIG
            # ==============================

            TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

            ADMIN_IDS = [
                123456789  # ← replace later with your Telegram numeric ID
                ]

                # ==============================
                # CORE LOGIC
                # ==============================

                class MakariCore:
                    def risk_score(self):
                            indicators = [
                                        0.5, 0.4, 0.3, 0.6,
                                                    0.7, 0.5, 0.4,
                                                                0.8, 0.7, 0.6,
                                                                            0.5, 0.4, 0.6
                                                                                    ]
                                                                                            return round(sum(indicators) / len(indicators), 2)

                                                                                                def decision(self, score):
                                                                                                        if score < 0.4:
                                                                                                                    return "PROCEED"
                                                                                                                            elif score < 0.7:
                                                                                                                                        return "PROCEED WITH CAUTION"
                                                                                                                                                else:
                                                                                                                                                            return "HOLD / REVIEW"

                                                                                                                                                            makari = MakariCore()
                                                                                                                                                            TASKS = []

                                                                                                                                                            # ==============================
                                                                                                                                                            # SECURITY
                                                                                                                                                            # ==============================

                                                                                                                                                            def is_admin(update: Update):
                                                                                                                                                                return update.effective_user.id in ADMIN_IDS

                                                                                                                                                                # ==============================
                                                                                                                                                                # COMMANDS
                                                                                                                                                                # ==============================

                                                                                                                                                                async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
                                                                                                                                                                    if not is_admin(update):
                                                                                                                                                                            return
                                                                                                                                                                                await update.message.reply_text(
                                                                                                                                                                                        "✅ MAKARI is ONLINE\n\n"
                                                                                                                                                                                                "Commands:\n"
                                                                                                                                                                                                        "/status\n"
                                                                                                                                                                                                                "/risk\n"
                                                                                                                                                                                                                        "/add_task <task>\n"
                                                                                                                                                                                                                                "/tasks"
                                                                                                                                                                                                                                    )

                                                                                                                                                                                                                                    async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
                                                                                                                                                                                                                                        if not is_admin(update):
                                                                                                                                                                                                                                                return
                                                                                                                                                                                                                                                    await update.message.reply_text("🟢 All MAKARI systems operational.")

                                                                                                                                                                                                                                                    async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
                                                                                                                                                                                                                                                        if not is_admin(update):
                                                                                                                                                                                                                                                                return
                                                                                                                                                                                                                                                                    score = makari.risk_score()
                                                                                                                                                                                                                                                                        decision = makari.decision(score)
                                                                                                                                                                                                                                                                            await update.message.reply_text(
                                                                                                                                                                                                                                                                                    f"📊 Risk Score: {score}\n📌 Decision: {decision}"
                                                                                                                                                                                                                                                                                        )

                                                                                                                                                                                                                                                                                        async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
                                                                                                                                                                                                                                                                                            if not is_admin(update):
                                                                                                                                                                                                                                                                                                    return
                                                                                                                                                                                                                                                                                                        if not context.args:
                                                                                                                                                                                                                                                                                                                await update.message.reply_text("Usage: /add_task <task>")
                                                                                                                                                                                                                                                                                                                        return
                                                                                                                                                                                                                                                                                                                            task = " ".join(context.args)
                                                                                                                                                                                                                                                                                                                                TASKS.append(task)
                                                                                                                                                                                                                                                                                                                                    await update.message.reply_text(f"✅ Task added:\n{task}")

                                                                                                                                                                                                                                                                                                                                    async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
                                                                                                                                                                                                                                                                                                                                        if not is_admin(update):
                                                                                                                                                                                                                                                                                                                                                return
                                                                                                                                                                                                                                                                                                                                                    if not TASKS:
                                                                                                                                                                                                                                                                                                                                                            await update.message.reply_text("📭 No active tasks.")
                                                                                                                                                                                                                                                                                                                                                                    return
                                                                                                                                                                                                                                                                                                                                                                        await update.message.reply_text(
                                                                                                                                                                                                                                                                                                                                                                                "📋 Tasks:\n" + "\n".join(f"- {t}" for t in TASKS)
                                                                                                                                                                                                                                                                                                                                                                                    )

                                                                                                                                                                                                                                                                                                                                                                                    # ==============================
                                                                                                                                                                                                                                                                                                                                                                                    # APP
                                                                                                                                                                                                                                                                                                                                                                                    # ==============================

                                                                                                                                                                                                                                                                                                                                                                                    async def main():
                                                                                                                                                                                                                                                                                                                                                                                        if not TOKEN:
                                                                                                                                                                                                                                                                                                                                                                                                raise RuntimeError("TELEGRAM_BOT_TOKEN not set")

                                                                                                                                                                                                                                                                                                                                                                                                    app = ApplicationBuilder().token(TOKEN).build()

                                                                                                                                                                                                                                                                                                                                                                                                        app.add_handler(CommandHandler("start", start))
                                                                                                                                                                                                                                                                                                                                                                                                            app.add_handler(CommandHandler("status", status))
                                                                                                                                                                                                                                                                                                                                                                                                                app.add_handler(CommandHandler("risk", risk))
                                                                                                                                                                                                                                                                                                                                                                                                                    app.add_handler(CommandHandler("add_task", add_task))
                                                                                                                                                                                                                                                                                                                                                                                                                        app.add_handler(CommandHandler("tasks", tasks))

                                                                                                                                                                                                                                                                                                                                                                                                                            print("🤖 MAKARI is running...")
                                                                                                                                                                                                                                                                                                                                                                                                                                await app.run_polling()

                                                                                                                                                                                                                                                                                                                                                                                                                                if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                                                                                                                                                    asyncio.run(main())