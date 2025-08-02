from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, ContextTypes
import random, asyncio
import logging

CHOICE_TOSS = 1
CHOICE_MATCH = 2
TOKEN = "8049920020:AAFLGKE0YuOfrRvo2ip4W74djSJdCtjVA-U"

#looging
logging.basicConfig(level=logging.INFO)

# Start Command
async def start(update: Update, context: CallbackContext):
    username = update.message.from_user.first_name
    await update.message.reply_text(f"<b>HI! {username}</b>",parse_mode="HTML")
    await update.message.reply_text(f"<i><b>HELLO! I  AM YOGI TELEGRAM BOT 🤖.\n Use /help FOR MORE OPTIONS.</b></i>",parse_mode="HTML")

# Cancel Command
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("<i><b>PREVIOUS COMMAND CANCELED. YOU CAN START AGAIN ANYTIME!</b></i>",parse_mode="HTML")
    context.user_data.clear()
    return ConversationHandler.END

# Help Command
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("<i><b> /start >> TO START BOT  \n  /toss >> TO TOSS A COIN \n  /match >>  TO PLAY SUPEROVER MATCH \n /cancel >> IF REVOKE ANY COMMAND </b></i>",parse_mode="HTML")

async def inv_cmd(update: Update,context: CallbackContext):
    await update.message.reply_text("<b> INVALID COMMAND PLS  FOLLOW BELOW INSTRUCTIONS</b>",parse_mode="HTML")
    await help_command(update,context)

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    await update.message.reply_text(f"<i><b>FOR MORE ENQUERY PLS USE >> /help</b></i>", parse_mode="HTML")

# ✅ **Toss Command**
async def Toss(update: Update, context: CallbackContext):
    await update.message.reply_text(f"<i><b>ENTER YOUR CHOICE: HEAD or TAIL </b></i>",parse_mode="HTML")
    return CHOICE_TOSS

# ✅ **Toss Handler**
async def Toss_handler(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    if user_message not in ["head", "tail"]:
        await update.message.reply_text(f"<i><b>INVALID CHOICE ! PLEASE TYPE HEAD OR TAIL.</b></i>",parse_mode="HTML")
        return CHOICE_TOSS
    
    await update.message.reply_animation("https://media.tenor.com/bd3puNXKLwUAAAAM/coin-toss.gif")

    toss_result = random.choice(["head", "tail"])

    await asyncio.sleep(2)

    if toss_result == "head":
        await update.message.reply_photo("https://tse4.mm.bing.net/th/id/OIP.eiGSAvRxCH62eIqWYy2_qQHaHa")
    else:
        await update.message.reply_photo("https://en.numista.com/catalogue/photos/inde/3180-original.jpg")


    if toss_result == user_message:
        await update.message.reply_text(f"<b>TOSS RESULT : {toss_result.upper()} 🎉 YOU WON THE TOSS!</b> \n TYPE /match <i><b>TO START THE MATCH.</b></i>",parse_mode="HTML")
        context.user_data["toss_winner"] = "user"
        return ConversationHandler.END
    else:
        bot_choice = random.choice(["bat", "ball"])
        await update.message.reply_text(f"<b>TOSS RESULT: {toss_result.upper()} 😞 YOU LOSS THE TOSS! \n BOT CHOOSE TO {bot_choice} FIRST</b>.\n<i><b>Type /match TO START THE GAME.</b></i>",parse_mode="HTML")
        context.user_data["toss_winner"] = "bot"
        context.user_data["first_innings"] = bot_choice  # Store bot's choice
        if bot_choice=='bat':
            context.user_data['bot_start']='bat'
            context.user_data['user_start']='ball'
        else:
            context.user_data['bot_start']='ball'
            context.user_data['user_start']='bat'
        return ConversationHandler.END

# ✅ **Match Command**
async def Match_command(update: Update, context: CallbackContext):
    toss_winner = context.user_data.get("toss_winner")

    if not toss_winner:
        await update.message.reply_text("<b>YOU NEED TO TOSS FIRST! TYPE /toss TO START.</b>",parse_mode="HTML")
        return ConversationHandler.END  # Exit if toss wasn't done

    if toss_winner == "user":
        await update.message.reply_text("<b>YOU WON THE TOSS! CHOOSE BAT OR BALL.</b>",parse_mode="HTML")
        return CHOICE_MATCH  # Wait for user input
    else:
        k=context.user_data.get("first_innings")
        await update.message.reply_text(f"<b>BOT HAS ALREADY WON THE TOSS AND CHOOSE TO {k.upper()} FIRST.</b>",parse_mode="HTML")
        await Match_handle_message(update, context)  # Call match directly
        return ConversationHandler.END

# ✅ **Match Handler**
async def Match_handle_message(update: Update, context: CallbackContext):
    if "first_innings" not in context.user_data:
        user_choice = update.message.text.lower()
        if user_choice not in ["bat", "ball"]:
            await update.message.reply_text("INVALID TYPE , CHOOSE BAT OR BALL.")
            return CHOICE_MATCH

        context.user_data["first_innings"] = user_choice  # Store user's choice
        context.user_data["user_choice"] = user_choice
        if user_choice=='bat':
            context.user_data['bot_start']='ball'
            context.user_data['user_start']='bat'
        else:
            context.user_data['bot_start']='bat'
            context.user_data['user_start']='ball'
    else:
        bot_choice = context.user_data["first_innings"]  # Retrieve stored choice
        user_choice = context.user_data.get("user_choice")


    bat_s, ball_s = 0, 0



    # ✅ First Batting
    await update.message.reply_text("<b>FIRST INNINGS START🏏</b>",parse_mode="HTML")
    wk1=0
    i=0
    lst1=[]
    await asyncio.sleep(2)
    while i<6:
        await update.message.reply_text("🥎")
        await update.message.reply_text(str(i+1)+"<b> BALL >> </b>",parse_mode="HTML")
        await asyncio.sleep(2)
        runs = random.choice([0,1,2,3,4,6,'WD','WKT'])
        lst1.append(str(runs))
        ls=['WD','WKT']
        if runs not in ls:
           await update.message.reply_text(str(runs) + "<b> RUNS</b>",parse_mode="HTML")
           bat_s += runs
        elif runs=='WKT':
            wk1+=1
            await update.message.reply_text("🚾 WKT GYA WKT 🚾")
            if wk1==2:
                await update.message.reply_text("<b> ALL OUT </b>",parse_mode="HTML")
                await update.message.reply_text(f"<b>SCORE=</b>"+str(bat_s)+"/"+str(wk1),parse_mode="HTML")
                break
        else :
            bat_s+=1
            i=i-1
            await update.message.reply_text("<b> WIDE BALL ✔</b>",parse_mode="HTML")
        await update.message.reply_text(f"<b>SCORE=</b>"+str(bat_s)+"/"+str(wk1),parse_mode="HTML")
        i+=1
    await asyncio.sleep(2)

    await update.message.reply_text(f"<b>FIRST INNINGS SCORE: {bat_s}</b>",parse_mode="HTML")
    await update.message.reply_text(f"<b>FIRST INNINGS SCORECARD:\n{'  '.join(lst1)}</b>",parse_mode="HTML")

    if context.user_data.get("bot_start",False)==False:
        k=context.user_data.get("user_start")
        if k=="bat":
            await update.message.reply_text(f"<b> BOT NEED:  {bat_s+1}  RUNS TO WIN THE MATCH</b>",parse_mode="HTML")
        else:
            await update.message.reply_text(f"<b> YOU NEED:  {bat_s+1} RUNS TO WIN THE MATCH</b>",parse_mode="HTML")

    else:
        k=context.user_data.get("bot_start")
        if k=="bat":
            await update.message.reply_text(f"<b> YOU NEED: {bat_s+1} RUNS TO WIN THE MATCH</b>",parse_mode="HTML")
        else:
            await update.message.reply_text(f"<b> BOOT NEED: {bat_s+1} RUNS TO WIN THE MATCH</b>",parse_mode="HTML")

    await asyncio.sleep(2)


    # ✅ Second Batting
    await update.message.reply_text("<b>SECOND INNINGS START🏏</b>",parse_mode="HTML")
    wk2=0
    i=0
    lst2=[]
    await asyncio.sleep(2)
    while i<6:
        await update.message.reply_text("🥎")
        await update.message.reply_text(str(i+1)+"<b> BALL >> </b>",parse_mode="HTML")
        await asyncio.sleep(1)
        runs = random.choice([0,1,2,3,4,6,'WD','WKT'])
        lst2.append(str(runs))
        ls=['WD','WKT']
        if runs not in ls:
           await update.message.reply_text(str(runs)+"<b> RUNS</b>",parse_mode="HTML")
           ball_s += runs
        elif runs=='WKT':
            wk2+=1
            await update.message.reply_text("🚾 WKT GYA WKT 🚾")
            if wk2==2:
                await update.message.reply_text("<b> ALL OUT </b>",parse_mode="HTML")
                await update.message.reply_text(f"<b>SCORE=</b>"+str(ball_s)+"/"+str(wk2),parse_mode="HTML")
                break
        else :
            ball_s+=1
            i=i-1
            await update.message.reply_text("<b> WIDE BALL ✔</b>",parse_mode="HTML")
        await update.message.reply_text(f"<b>SCORE=</b>"+str(ball_s)+"/"+str(wk2),parse_mode="HTML")
        if ball_s>bat_s:
           break
        i+=1
    await asyncio.sleep(2)

    await update.message.reply_text(f"<b>SECOND INNINGS SCORE: {ball_s} </b>",parse_mode="HTML")
    await update.message.reply_text(f"<b>SECOND INNINGS SCORECARD:\n{'  '.join(lst2)}</b>",parse_mode="HTML")
    await asyncio.sleep(2)
    # ✅ Determine Winner
    if context.user_data["toss_winner"]=="bot":
        if bot_choice == "bat":
          bot_s = bat_s
          user_s = ball_s
        else:
           bot_s = ball_s
           user_s = bat_s

    else:
        if user_choice == "bat":
          user_s = bat_s
          bot_s = ball_s
        else:
           user_s = ball_s
           bot_s = bat_s
    if bot_s > user_s:
        if context.user_data.get("bot_start")=="bat":
            await update.message.reply_text("😔")
            await update.message.reply_text(f"<b>BOT  WON THE MATCH 🏏 by {bot_s - user_s} runs!</b>", parse_mode="HTML")
        else :
            await update.message.reply_text("😔")
            await update.message.reply_text(f"<b>BOT WON THE MATCH 🏏 by {2 -wk2} WICKETS!</b>", parse_mode="HTML")


    elif user_s > bot_s:
        if context.user_data.get("user_start")=="bat":
            await update.message.reply_text("😍")
            await update.message.reply_text(f"<b>YOU WON THE MATCH 🏏 by {user_s - bot_s} runs!</b>", parse_mode="HTML")
        else:
            await update.message.reply_text("😍")
            await update.message.reply_text(f"<b>YOU WON THE MATCH 🏏 by {2 - wk2} WICKETS!</b>", parse_mode="HTML")
    else:
        await update.message.reply_text(f"<b>THE MATCH IS TIE!</b>",parse_mode="HTML")
    context.user_data.clear()
    return ConversationHandler.END

# ✅ **Main Function**
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    toss_handler = ConversationHandler(
        entry_points=[CommandHandler("toss", Toss)],
        states={CHOICE_TOSS: [MessageHandler(filters.TEXT & ~filters.COMMAND, Toss_handler)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    match_handler = ConversationHandler(
        entry_points=[CommandHandler("match", Match_command)],
        states={CHOICE_MATCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, Match_handle_message)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(toss_handler)
    app.add_handler(match_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, inv_cmd))


    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
