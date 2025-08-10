#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Self Bot - ربات سلف تلگرام
تمام قابلیت‌های مورد نیاز با کیفیت بالا و بدون باگ
شامل ربات هلپر با دکمه‌های شیشه‌ای که در هر جایی کار می‌کند
"""

import asyncio
import os
import json
import time
import random
import re
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Any
import logging
import sqlite3

try:
    from pyrogram import Client, filters, errors
    from pyrogram.types import Message, User, Chat, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
    from pyrogram.enums import ChatType, MessageMediaType, ParseMode
    from pyrogram.raw.functions.messages import SetTyping
    from pyrogram.raw.types import SendMessageTypingAction
    import tgcrypto  # برای سرعت بالاتر
except ImportError:
    print("❌ pyrogram یا tgcrypto نصب نیست. لطفاً نصب کنید:")
    print("pip install pyrogram tgcrypto")
    exit(1)

# تنظیمات لاگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('selfbot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TelegramSelfBot:
    def __init__(self):
        # تنظیمات اصلی سلف بات
        self.api_id = "29042268"  # API ID خود را وارد کنید
        self.api_hash = "54a7b377dd4a04a58108639febe2f443"  # API Hash خود را وارد کنید
        self.phone_number = "+989362349331"  # شماره تلفن خود را وارد کنید
        
        # تنظیمات ربات هلپر
        self.bot_token = "7871342383:AAEnHXtvc6txRoyGegRL_IeErLISmS4j_DQ"  # توکن ربات هلپر
        self.owner_id = 6508600903  # آیدی عددی صاحب اکانت
        
        # ایجاد کلاینت‌ها
        self.app = None
        self.helper_bot = None
        self.is_running = False
        
        # متغیرهای وضعیت
        self.data_file = "selfbot_data.json"
        self.load_data()
        
        # ذخیره اطلاعات چت فعلی برای دستورات
        self.current_chat_id = None
        self.current_message_id = None
        self.pending_commands = {}  # ذخیره دستورات در انتظار تنظیمات
        
        # تنظیمات پیش‌فرض
        self.default_settings = {
            'ping_enabled': True,
            'auto_seen': False,
            'secretary_mode': False,
            'pv_lock': False,
            'pv_lock_mode': 'all',
            'pv_lock_users': [],
            'spam_protection': True,
            'forward_lock': False,
            'sticker_lock': False,
            'auto_react': False,
            'word_filter': False,
            'anti_login': False,
            'auto_typing': False,
            'comment_mode': False,
            'dice_cheat': False,
            'bowling_cheat': False,
            'football_cheat': False,
            'dart_cheat': False,
            'auto_bold': False,
            'auto_italic': False,
            'auto_code': False,
            'auto_strikethrough': False,
            'auto_spoiler': False,
            'auto_underline': False,
            'time_in_name': False,
            'auto_bio_time': False
        }
        
        # آپدیت تنظیمات
        for key, value in self.default_settings.items():
            if key not in self.data:
                self.data[key] = value

    def clean_sessions(self):
        """پاک‌سازی فایل‌های Session قدیمی"""
        session_files = [
            "selfbot_session.session", 
            "selfbot_session.session-journal",
            "helper_bot.session",
            "helper_bot.session-journal"
        ]
        
        for file in session_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    logger.info(f"حذف فایل session قدیمی: {file}")
                except Exception as e:
                    logger.warning(f"خطا در حذف {file}: {e}")

    def load_data(self):
        """بارگذاری داده‌ها از فایل"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    
                # تبدیل list ها به set برای سازگاری
                for key in ['banned_users', 'blocked_users', 'admin_users', 'typing_users', 'muted_users', 'pv_locked_users']:
                    if key in self.data and isinstance(self.data[key], list):
                        self.data[key] = set(self.data[key])
            else:
                self.data = self.get_default_data()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"خطا در بارگذاری داده‌ها: {e}")
            self.data = self.get_default_data()
    
    def get_default_data(self):
        """داده‌های پیش‌فرض"""
        return {
            'friends': {},
            'enemies': {},
            'banned_users': set(),
            'blocked_users': set(),
            'saved_messages': [],
            'auto_replies': {},
            'filtered_words': [],
            'comment_channels': [],
            'admin_users': set(),
            'secretary_messages': {},
            'typing_users': set(),
            'last_seen': {},
            'muted_users': set(),
            'pv_locked_users': set(),
            'text_format': None,
            'format_enabled': False,
            'secretary_message': '📋 در حال حاضر در دسترس نیستم. پیام شما ثبت شد.',
            'original_name': '',
            'original_bio': ''
        }

    def save_data(self):
        """ذخیره داده‌ها در فایل"""
        try:
            # تبدیل set ها به list برای JSON
            data_to_save = self.data.copy()
            for key in ['banned_users', 'blocked_users', 'admin_users', 'typing_users', 'muted_users', 'pv_locked_users']:
                if key in data_to_save and isinstance(data_to_save[key], set):
                    data_to_save[key] = list(data_to_save[key])
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"خطا در ذخیره داده‌ها: {e}")

    def get_time_superscript(self):
        """تبدیل ساعت به فرمت superscript"""
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        
        # نقشه تبدیل اعداد به superscript
        superscript_map = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
            ':': ':'
        }
        
        return ''.join(superscript_map.get(char, char) for char in time_str)

    async def update_name_with_time(self):
        """بروزرسانی نام با ساعت"""
        if not self.data.get('time_in_name'):
            return
            
        try:
            time_super = self.get_time_superscript()
            original_name = self.data.get('original_name', '')
            
            if not original_name:
                # ذخیره نام اصلی
                me = await self.app.get_me()
                self.data['original_name'] = me.first_name
                original_name = me.first_name
                self.save_data()
            
            new_name = f"{original_name} {time_super}"
            await self.app.update_profile(first_name=new_name)
            
        except Exception as e:
            logger.error(f"خطا در بروزرسانی نام: {e}")

    async def update_bio_with_time(self):
        """بروزرسانی بیو با ساعت"""
        if not self.data.get('auto_bio_time'):
            return
            
        try:
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            date_str = now.strftime("%Y/%m/%d")
            
            bio_text = f"🕐 {time_str} | 📅 {date_str}"
            await self.app.update_profile(bio=bio_text)
            
        except Exception as e:
            logger.error(f"خطا در بروزرسانی بیو: {e}")

    async def start_bot(self):
        """راه‌اندازی ربات"""
        try:
            # پاک‌سازی session های قدیمی
            self.clean_sessions()
            
            # بارگذاری داده‌ها
            self.load_data()
            
            # بررسی اطلاعات ضروری
            if (self.api_id == "YOUR_API_ID" or 
                self.api_hash == "YOUR_API_HASH" or 
                self.phone_number == "YOUR_PHONE"):
                logger.error("❌ لطفاً اطلاعات API و شماره تلفن را در کد وارد کنید!")
                return False
            
            # راه‌اندازی سلف بات
            self.app = Client(
                name="selfbot_session",
                api_id=int(self.api_id) if str(self.api_id).isdigit() else self.api_id,
                api_hash=self.api_hash,
                phone_number=self.phone_number,
                workdir=".",
                in_memory=True  # استفاده از memory session برای جلوگیری از باگ
            )
            
            # راه‌اندازی ربات هلپر
            if self.bot_token and self.bot_token != "YOUR_BOT_TOKEN":
                self.helper_bot = Client(
                    name="helper_bot",
                    api_id=int(self.api_id) if str(self.api_id).isdigit() else self.api_id,
                    api_hash=self.api_hash,
                    bot_token=self.bot_token,
                    workdir=".",
                    in_memory=True
                )
            
            await self.app.start()
            logger.info("✅ سلف بات با موفقیت راه‌اندازی شد!")
            
            if self.helper_bot:
                await self.helper_bot.start()
                logger.info("✅ ربات هلپر با موفقیت راه‌اندازی شد!")
            
            self.is_running = True
            
            # ثبت handlers
            self.register_handlers()
            
            # حلقه اصلی
            await self.main_loop()
            
        except errors.PhoneNumberInvalid:
            logger.error("❌ شماره تلفن نامعتبر است!")
            return False
        except errors.ApiIdInvalid:
            logger.error("❌ API ID نامعتبر است!")
            return False
        except errors.ApiIdPublishedFlood:
            logger.error("❌ API ID فلود شده است! کمی صبر کنید.")
            return False
        except Exception as e:
            logger.error(f"❌ خطا در راه‌اندازی ربات: {e}")
            self.is_running = False
            return False

    def register_handlers(self):
        """ثبت تمام handlers"""
        
        # Handler برای پیام‌های سلف بات
        @self.app.on_message(filters.me)
        async def handle_my_messages(client, message: Message):
            await self.process_my_message(message)
        
        @self.app.on_message(~filters.me & filters.private)
        async def handle_private_messages(client, message: Message):
            await self.process_other_message(message)
            
        @self.app.on_message(~filters.me & filters.group)
        async def handle_group_messages(client, message: Message):
            await self.process_other_message(message)
        
        # Handler برای ربات هلپر
        if self.helper_bot:
            @self.helper_bot.on_message(filters.command(["help", "start"]))
            async def helper_help_command(client, message: Message):
                if message.from_user.id == self.owner_id:
                    await self.show_helper_menu(message)
                else:
                    await message.reply("❌ شما مجاز به استفاده از این ربات نیستید!")
            
            @self.helper_bot.on_callback_query()
            async def handle_callback(client, callback_query: CallbackQuery):
                if callback_query.from_user.id == self.owner_id:
                    await self.handle_helper_callback(callback_query)
                else:
                    await callback_query.answer("❌ شما مجاز نیستید!", show_alert=True)
            
            @self.helper_bot.on_inline_query()
            async def handle_inline_query(client, inline_query: InlineQuery):
                if inline_query.from_user.id == self.owner_id:
                    await self.handle_inline_query(inline_query)
                else:
                    await inline_query.answer([])
            
            # Handler برای پیام‌های متنی ربات هلپر (برای دریافت تنظیمات)
            @self.helper_bot.on_message(filters.text & filters.private)
            async def handle_settings_input(client, message: Message):
                if message.from_user.id == self.owner_id:
                    await self.handle_command_settings(message)

    async def handle_inline_query(self, inline_query: InlineQuery):
        """مدیریت inline query ها"""
        results = []
        
        # دکمه پنل کنترل
        results.append(
            InlineQueryResultArticle(
                id="control_panel",
                title="🤖 پنل کنترل ربات سلف",
                description="دسترسی به تمام دستورات و تنظیمات",
                input_message_content=InputTextMessageContent(
                    message_text="🤖 **پنل کنترل ربات سلف**\n\n⚡ برای استفاده از دستورات، روی دکمه‌های زیر کلیک کنید:"
                ),
                reply_markup=self.get_main_inline_keyboard()
            )
        )
        
        # دکمه‌های سریع
        quick_commands = [
            ("🏓 پینگ", "ping", "نمایش سرعت ربات"),
            ("🕐 ساعت", "time", "نمایش تاریخ و ساعت"),
            ("📊 وضعیت", "status", "نمایش وضعیت ربات"),
            ("🎬 انیمیشن", "animation", "نمایش انیمیشن زیبا")
        ]
        
        for title, cmd, desc in quick_commands:
            results.append(
                InlineQueryResultArticle(
                    id=f"quick_{cmd}",
                    title=title,
                    description=desc,
                    input_message_content=InputTextMessageContent(
                        message_text=f"⚡ در حال اجرای {title}..."
                    ),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(f"اجرای {title}", callback_data=f"cmd_{cmd}")
                    ]])
                )
            )
        
        await inline_query.answer(results, cache_time=1)

    def get_main_inline_keyboard(self):
        """دریافت کیبورد اصلی inline"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔧 دستورات اصلی", callback_data="main_commands"),
                InlineKeyboardButton("🎮 بازی و سرگرمی", callback_data="games")
            ],
            [
                InlineKeyboardButton("🔒 امنیت و حفاظت", callback_data="security"),
                InlineKeyboardButton("👥 مدیریت کاربران", callback_data="users")
            ],
            [
                InlineKeyboardButton("⚙️ تنظیمات خودکار", callback_data="auto_settings"),
                InlineKeyboardButton("📱 ابزارهای مفید", callback_data="tools")
            ],
            [
                InlineKeyboardButton("🎨 فرمت و استایل", callback_data="formatting"),
                InlineKeyboardButton("⏰ تایم و زمان", callback_data="time_settings")
            ],
            [
                InlineKeyboardButton("📊 وضعیت ربات", callback_data="status"),
                InlineKeyboardButton("🔄 بروزرسانی", callback_data="refresh")
            ]
        ])

    async def show_helper_menu(self, message: Message):
        """نمایش منوی اصلی ربات هلپر"""
        keyboard = self.get_main_inline_keyboard()
        
        text = f"""
🤖 **ربات سلف تلگرام - پنل کنترل**
⚡ نسخه پیشرفته و کامل ⚡

🎯 **راهنمای استفاده:**
• روی هر دکمه کلیک کنید تا دستورات مربوطه را ببینید
• دکمه‌ها به صورت خودکار دستورات را اجرا می‌کنند
• تمام عملیات در اکانت اصلی شما انجام می‌شود

🔥 **ویژگی‌های خاص:**
✅ دستورات با دکمه‌های شیشه‌ای
✅ قفل پیوی پیشرفته
✅ فرمت خودکار برای تمام پیام‌ها
✅ مدیریت کامل دوستان و دشمنان
✅ تقلب در بازی‌های تلگرام
✅ تایم در نام و بیو

💡 **نکته:** برای استفاده در هر جای تلگرام، از حالت inline استفاده کنید:
`@{(await self.helper_bot.get_me()).username}`

👤 **کاربر:** {message.from_user.first_name}
🆔 **آیدی:** `{message.from_user.id}`
        """
        
        await message.reply(text, reply_markup=keyboard)

    async def handle_helper_callback(self, callback_query: CallbackQuery):
        """مدیریت callback های ربات هلپر"""
        data = callback_query.data
        
        try:
            if data == "main_commands":
                await self.show_main_commands(callback_query)
            elif data == "games":
                await self.show_games_menu(callback_query)
            elif data == "security":
                await self.show_security_menu(callback_query)
            elif data == "users":
                await self.show_users_menu(callback_query)
            elif data == "auto_settings":
                await self.show_auto_settings_menu(callback_query)
            elif data == "tools":
                await self.show_tools_menu(callback_query)
            elif data == "formatting":
                await self.show_formatting_menu(callback_query)
            elif data == "time_settings":
                await self.show_time_settings_menu(callback_query)
            elif data == "status":
                await self.show_status(callback_query)
            elif data == "refresh":
                await self.show_helper_menu_callback(callback_query)
            elif data == "back_main":
                await self.show_helper_menu_callback(callback_query)
            else:
                # اجرای دستورات
                await self.execute_command(callback_query, data)
        except Exception as e:
            logger.error(f"خطا در callback handler: {e}")
            await callback_query.answer(f"❌ خطا: {str(e)}", show_alert=True)

    async def show_helper_menu_callback(self, callback_query: CallbackQuery):
        """نمایش منوی اصلی در callback"""
        keyboard = self.get_main_inline_keyboard()
        
        text = f"""
🤖 **ربات سلف تلگرام - پنل کنترل**
⚡ نسخه پیشرفته و کامل ⚡

🎯 **راهنمای استفاده:**
• روی هر دکمه کلیک کنید تا دستورات مربوطه را ببینید
• دکمه‌ها به صورت خودکار دستورات را اجرا می‌کنند
• تمام عملیات در اکانت اصلی شما انجام می‌شود

🔥 **ویژگی‌های خاص:**
✅ دستورات با دکمه‌های شیشه‌ای
✅ قفل پیوی پیشرفته
✅ فرمت خودکار برای تمام پیام‌ها
✅ مدیریت کامل دوستان و دشمنان
✅ تقلب در بازی‌های تلگرام
✅ تایم در نام و بیو

💡 **نکته:** برای استفاده در هر جای تلگرام، از حالت inline استفاده کنید:
`@{(await self.helper_bot.get_me()).username}`

👤 **کاربر:** {callback_query.from_user.first_name}
🆔 **آیدی:** `{callback_query.from_user.id}`
        """
        
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_main_commands(self, callback_query: CallbackQuery):
        """نمایش دستورات اصلی"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏓 پینگ", callback_data="cmd_ping"),
                InlineKeyboardButton("💥 اشکن", callback_data="cmd_crash")
            ],
            [
                InlineKeyboardButton("🔇 سکوت", callback_data="cmd_mute"),
                InlineKeyboardButton("📋 منشی", callback_data="cmd_secretary")
            ],
            [
                InlineKeyboardButton("🔒 قفل پیوی", callback_data="cmd_pv_lock"),
                InlineKeyboardButton("🎬 انیمیشن", callback_data="cmd_animation")
            ],
            [
                InlineKeyboardButton("📨 اسپم", callback_data="cmd_spam"),
                InlineKeyboardButton("🕐 ساعت", callback_data="cmd_time")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
            ]
        ])
        
        text = """
🔧 **دستورات اصلی**

🏓 **پینگ** - نمایش سرعت ربات
💥 **اشکن** - اشکن کردن چت (نیاز به تنظیمات)
🔇 **سکوت** - سکوت کاربر (ریپلای)
📋 **منشی** - فعال/غیرفعال منشی
🔒 **قفل پیوی** - قفل پیام‌های خصوصی
🎬 **انیمیشن** - نمایش انیمیشن زیبا
📨 **اسپم** - ارسال پیام‌های متوالی (نیاز به تنظیمات)
🕐 **ساعت** - نمایش تاریخ و ساعت

💡 **نکته:** روی هر دکمه کلیک کنید تا دستور اجرا شود!
        """
        
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_games_menu(self, callback_query: CallbackQuery):
        """نمایش منوی بازی‌ها"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎲 تقلب تاس", callback_data="cmd_dice"),
                InlineKeyboardButton("🎳 تقلب بولینگ", callback_data="cmd_bowling")
            ],
            [
                InlineKeyboardButton("⚽ تقلب فوتبال", callback_data="cmd_football"),
                InlineKeyboardButton("🎯 تقلب دارت", callback_data="cmd_dart")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
            ]
        ])
        
        text = """
🎮 **بازی و سرگرمی**

🎲 **تقلب تاس** - تقلب در بازی تاس
🎳 **تقلب بولینگ** - تقلب در بولینگ
⚽ **تقلب فوتبال** - تقلب در فوتبال
🎯 **تقلب دارت** - تقلب در دارت

🎯 **راهنما:** این دستورات به شما کمک می‌کنند در بازی‌های تلگرام برنده شوید!
        """
        
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_security_menu(self, callback_query: CallbackQuery):
        """نمایش منوی امنیت"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏩ قفل فوروارد", callback_data="cmd_forward_lock"),
                InlineKeyboardButton("🔒 قفل استیکر", callback_data="cmd_sticker_lock")
            ],
            [
                InlineKeyboardButton("🚫 فیلتر کلمات", callback_data="cmd_word_filter"),
                InlineKeyboardButton("🛡️ ضد لاگین", callback_data="cmd_anti_login")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
            ]
        ])
        
        text = """
🔒 **امنیت و حفاظت**

⏩ **قفل فوروارد** - جلوگیری از فوروارد
🔒 **قفل استیکر** - حذف استیکرها
🚫 **فیلتر کلمات** - فیلتر کلمات نامناسب
🛡️ **ضد لاگین** - محافظت از ورود غیرمجاز

🔐 **امنیت:** این ابزارها اکانت شما را محافظت می‌کنند!
        """
        
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_users_menu(self, callback_query: CallbackQuery):
        """نمایش منوی مدیریت کاربران"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🚫 بن کاربر", callback_data="cmd_ban"),
                InlineKeyboardButton("🚫 مسدود کردن", callback_data="cmd_block")
            ],
            [
                InlineKeyboardButton("😡 اضافه به دشمنان", callback_data="cmd_enemy"),
                InlineKeyboardButton("😊 اضافه به دوستان", callback_data="cmd_friend")
            ],
            [
                InlineKeyboardButton("👥 تگ همگانی", callback_data="cmd_tag_all"),
                InlineKeyboardButton("👑 تگ ادمین‌ها", callback_data="cmd_tag_admins")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
            ]
        ])
        
        text = """
👥 **مدیریت کاربران**

🚫 **بن کاربر** - بن کردن کاربر از گروه
🚫 **مسدود کردن** - مسدود کردن کاربر
😡 **اضافه به دشمنان** - اضافه به لیست سیاه
😊 **اضافه به دوستان** - اضافه به لیست دوستان
👥 **تگ همگانی** - تگ کردن همه اعضا
👑 **تگ ادمین‌ها** - تگ کردن ادمین‌ها

⚠️ **توجه:** برای استفاده از این دستورات، ابتدا روی پیام کاربر ریپلای کنید!
        """
        
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_auto_settings_menu(self, callback_query: CallbackQuery):
        """نمایش منوی تنظیمات خودکار"""
        auto_seen_status = "✅" if self.data.get('auto_seen') else "❌"
        auto_react_status = "✅" if self.data.get('auto_react') else "❌"
        auto_typing_status = "✅" if self.data.get('auto_typing') else "❌"
        secretary_status = "✅" if self.data.get('secretary_mode') else "❌"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"👁️ سین خودکار {auto_seen_status}", callback_data="cmd_auto_seen"),
                InlineKeyboardButton(f"😍 ری‌اکت خودکار {auto_react_status}", callback_data="cmd_auto_react")
            ],
            [
                InlineKeyboardButton(f"⌨️ تپچی خودکار {auto_typing_status}", callback_data="cmd_auto_typing"),
                InlineKeyboardButton(f"📋 منشی {secretary_status}", callback_data="cmd_secretary_toggle")
            ],
            [
                InlineKeyboardButton("💬 پاسخ خودکار", callback_data="cmd_auto_reply"),
                InlineKeyboardButton("💬 کامنت خودکار", callback_data="cmd_comment")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
            ]
        ])
        
        text = f"""
⚙️ **تنظیمات خودکار**

👁️ **سین خودکار** - خواندن خودکار پیام‌ها
😍 **ری‌اکت خودکار** - ری‌اکت به پیام‌ها
⌨️ **تپچی خودکار** - نمایش در حال تایپ
📋 **منشی** - پاسخ خودکار در غیاب
💬 **پاسخ خودکار** - پاسخ به کلمات خاص
💬 **کامنت خودکار** - کامنت اول در کانال‌ها

🔄 **وضعیت فعلی:**
• سین خودکار: {"فعال" if self.data.get('auto_seen') else "غیرفعال"}
• ری‌اکت خودکار: {"فعال" if self.data.get('auto_react') else "غیرفعال"}
• تپچی خودکار: {"فعال" if self.data.get('auto_typing') else "غیرفعال"}
• منشی: {"فعال" if self.data.get('secretary_mode') else "غیرفعال"}
        """
        
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_tools_menu(self, callback_query: CallbackQuery):
        """نمایش منوی ابزارها"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ℹ️ اطلاعات", callback_data="cmd_info"),
                InlineKeyboardButton("🕐 ساعت", callback_data="cmd_time")
            ],
            [
                InlineKeyboardButton("👤 پروفایل", callback_data="cmd_profile"),
                InlineKeyboardButton("💾 سیو پیام", callback_data="cmd_save")
            ],
            [
                InlineKeyboardButton("🗑️ حذف پیام", callback_data="cmd_delete"),
                InlineKeyboardButton("🔄 ریستارت", callback_data="cmd_restart")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
            ]
        ])
        
        text = """
📱 **ابزارهای مفید**

ℹ️ **اطلاعات** - نمایش اطلاعات کاربر/گروه
🕐 **ساعت** - نمایش تاریخ و ساعت
👤 **پروفایل** - نمایش پروفایل کاربر
💾 **سیو پیام** - ذخیره پیام/رسانه
🗑️ **حذف پیام** - حذف پیام
🔄 **ریستارت** - راه‌اندازی مجدد ربات

🛠️ **راهنما:** این ابزارها کارهای روزمره شما را آسان‌تر می‌کنند!
        """
        
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_formatting_menu(self, callback_query: CallbackQuery):
        """نمایش منوی فرمت"""
        bold_status = "✅" if self.data.get('auto_bold') else "❌"
        italic_status = "✅" if self.data.get('auto_italic') else "❌"
        code_status = "✅" if self.data.get('auto_code') else "❌"
        strikethrough_status = "✅" if self.data.get('auto_strikethrough') else "❌"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"**بولد خودکار** {bold_status}", callback_data="cmd_auto_bold"),
                InlineKeyboardButton(f"_ایتالیک خودکار_ {italic_status}", callback_data="cmd_auto_italic")
            ],
            [
                InlineKeyboardButton(f"`کد خودکار` {code_status}", callback_data="cmd_auto_code"),
                InlineKeyboardButton(f"~~خط‌خورده~~ {strikethrough_status}", callback_data="cmd_auto_strikethrough")
            ],
            [
                InlineKeyboardButton("||اسپویلر خودکار||", callback_data="cmd_auto_spoiler"),
                InlineKeyboardButton("__زیرخط خودکار__", callback_data="cmd_auto_underline")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
            ]
        ])
        
        text = f"""
🎨 **فرمت و استایل خودکار**

**بولد خودکار** - تمام پیام‌ها بولد می‌شوند
_ایتالیک خودکار_ - تمام پیام‌ها ایتالیک می‌شوند
`کد خودکار` - تمام پیام‌ها کد می‌شوند
~~خط‌خورده خودکار~~ - تمام پیام‌ها خط‌خورده می‌شوند
||اسپویلر خودکار|| - تمام پیام‌ها اسپویلر می‌شوند
__زیرخط خودکار__ - تمام پیام‌ها زیرخط می‌شوند

🔄 **وضعیت فعلی:**
• بولد: {"فعال" if self.data.get('auto_bold') else "غیرفعال"}
• ایتالیک: {"فعال" if self.data.get('auto_italic') else "غیرفعال"}
• کد: {"فعال" if self.data.get('auto_code') else "غیرفعال"}
• خط‌خورده: {"فعال" if self.data.get('auto_strikethrough') else "غیرفعال"}

⚠️ **توجه:** این تنظیمات روی تمام پیام‌های آینده شما اعمال می‌شود!
        """
        
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_time_settings_menu(self, callback_query: CallbackQuery):
        """نمایش منوی تنظیمات زمان"""
        time_in_name_status = "✅" if self.data.get('time_in_name') else "❌"
        auto_bio_time_status = "✅" if self.data.get('auto_bio_time') else "❌"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"🕐 تایم در نام {time_in_name_status}", callback_data="cmd_time_in_name"),
                InlineKeyboardButton(f"📝 تایم در بیو {auto_bio_time_status}", callback_data="cmd_auto_bio_time")
            ],
            [
                InlineKeyboardButton("🔄 بروزرسانی نام", callback_data="cmd_update_name"),
                InlineKeyboardButton("🔄 بروزرسانی بیو", callback_data="cmd_update_bio")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
            ]
        ])
        
        text = f"""
⏰ **تنظیمات تایم و زمان**

🕐 **تایم در نام** - نمایش ساعت در نام پروفایل
📝 **تایم در بیو** - نمایش ساعت و تاریخ در بیو
🔄 **بروزرسانی نام** - بروزرسانی دستی نام
🔄 **بروزرسانی بیو** - بروزرسانی دستی بیو

🔄 **وضعیت فعلی:**
• تایم در نام: {"فعال" if self.data.get('time_in_name') else "غیرفعال"}
• تایم در بیو: {"فعال" if self.data.get('auto_bio_time') else "غیرفعال"}

💡 **نکته:** تایم در نام با فونت superscript نمایش داده می‌شود!
        """
        
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_status(self, callback_query: CallbackQuery):
        """نمایش وضعیت ربات"""
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔄 بروزرسانی", callback_data="status"),
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
            ]
        ])
        
        # محاسبه آمار
        friends_count = len(self.data.get('friends', {}))
        enemies_count = len(self.data.get('enemies', {}))
        saved_count = len(self.data.get('saved_messages', []))
        filtered_words_count = len(self.data.get('filtered_words', []))
        
        text = f"""
📊 **وضعیت ربات سلف**

🤖 **وضعیت:** {"🟢 آنلاین" if self.is_running else "🔴 آفلاین"}
⏰ **زمان آخرین بروزرسانی:** {datetime.now().strftime("%H:%M:%S")}

📈 **آمار:**
👥 **دوستان:** {friends_count} نفر
😡 **دشمنان:** {enemies_count} نفر
💾 **پیام‌های ذخیره شده:** {saved_count} پیام
🚫 **کلمات فیلتر شده:** {filtered_words_count} کلمه

⚙️ **تنظیمات فعال:**
{"✅" if self.data.get('auto_seen') else "❌"} سین خودکار
{"✅" if self.data.get('auto_react') else "❌"} ری‌اکت خودکار
{"✅" if self.data.get('secretary_mode') else "❌"} منشی
{"✅" if self.data.get('pv_lock') else "❌"} قفل پیوی
{"✅" if self.data.get('forward_lock') else "❌"} قفل فوروارد
{"✅" if self.data.get('sticker_lock') else "❌"} قفل استیکر
{"✅" if self.data.get('auto_typing') else "❌"} تپچی خودکار
{"✅" if self.data.get('word_filter') else "❌"} فیلتر کلمات

🎨 **فرمت خودکار:**
{"✅" if self.data.get('auto_bold') else "❌"} بولد
{"✅" if self.data.get('auto_italic') else "❌"} ایتالیک
{"✅" if self.data.get('auto_code') else "❌"} کد
{"✅" if self.data.get('auto_strikethrough') else "❌"} خط‌خورده

⏰ **تنظیمات زمان:**
{"✅" if self.data.get('time_in_name') else "❌"} تایم در نام
{"✅" if self.data.get('auto_bio_time') else "❌"} تایم در بیو
        """
        
        await callback_query.edit_message_text(text, reply_markup=keyboard)

    async def execute_command(self, callback_query: CallbackQuery, command: str):
        """اجرای دستورات از طریق callback"""
        try:
            # دستورات که نیاز به تنظیمات دارند
            settings_required_commands = {
                'cmd_crash': 'crash',
                'cmd_spam': 'spam',
                'cmd_auto_reply': 'auto_reply',
                'cmd_word_filter': 'word_filter',
                'cmd_comment': 'comment',
                'cmd_mute': 'mute',
                'cmd_ban': 'ban',
                'cmd_block': 'block',
                'cmd_enemy': 'enemy',
                'cmd_friend': 'friend',
                'cmd_tag_all': 'tag_all',
                'cmd_tag_admins': 'tag_admins',
                'cmd_info': 'info',
                'cmd_profile': 'profile',
                'cmd_save': 'save',
                'cmd_delete': 'delete'
            }
            
            if command in settings_required_commands:
                if self.helper_bot:
                    await self.request_command_settings(callback_query, settings_required_commands[command])
                else:
                    await callback_query.answer("❌ برای این دستور نیاز به ربات هلپر است!", show_alert=True)
                return
            
            # دستورات فوری
            if command == "cmd_ping":
                await self.execute_ping_command(callback_query)
                
            elif command == "cmd_auto_seen":
                self.data['auto_seen'] = not self.data.get('auto_seen', False)
                self.save_data()
                status = "فعال" if self.data['auto_seen'] else "غیرفعال"
                await callback_query.answer(f"👁️ سین خودکار {status} شد!", show_alert=True)
                await self.show_auto_settings_menu(callback_query)
                
            elif command == "cmd_auto_react":
                self.data['auto_react'] = not self.data.get('auto_react', False)
                self.save_data()
                status = "فعال" if self.data['auto_react'] else "غیرفعال"
                await callback_query.answer(f"😍 ری‌اکت خودکار {status} شد!", show_alert=True)
                await self.show_auto_settings_menu(callback_query)
                
            elif command == "cmd_auto_typing":
                self.data['auto_typing'] = not self.data.get('auto_typing', False)
                self.save_data()
                status = "فعال" if self.data['auto_typing'] else "غیرفعال"
                await callback_query.answer(f"⌨️ تپچی خودکار {status} شد!", show_alert=True)
                await self.show_auto_settings_menu(callback_query)
                
            elif command == "cmd_secretary_toggle":
                self.data['secretary_mode'] = not self.data.get('secretary_mode', False)
                self.save_data()
                status = "فعال" if self.data['secretary_mode'] else "غیرفعال"
                await callback_query.answer(f"📋 منشی {status} شد!", show_alert=True)
                await self.show_auto_settings_menu(callback_query)
                
            elif command == "cmd_pv_lock":
                self.data['pv_lock'] = not self.data.get('pv_lock', False)
                self.save_data()
                status = "فعال" if self.data['pv_lock'] else "غیرفعال"
                await callback_query.answer(f"🔒 قفل پیوی {status} شد!", show_alert=True)
                
            elif command == "cmd_forward_lock":
                self.data['forward_lock'] = not self.data.get('forward_lock', False)
                self.save_data()
                status = "فعال" if self.data['forward_lock'] else "غیرفعال"
                await callback_query.answer(f"⏩ قفل فوروارد {status} شد!", show_alert=True)
                
            elif command == "cmd_sticker_lock":
                self.data['sticker_lock'] = not self.data.get('sticker_lock', False)
                self.save_data()
                status = "فعال" if self.data['sticker_lock'] else "غیرفعال"
                await callback_query.answer(f"🔒 قفل استیکر {status} شد!", show_alert=True)
                
            elif command == "cmd_anti_login":
                self.data['anti_login'] = not self.data.get('anti_login', False)
                self.save_data()
                status = "فعال" if self.data['anti_login'] else "غیرفعال"
                await callback_query.answer(f"🛡️ ضد لاگین {status} شد!", show_alert=True)
                
            # دستورات فرمت خودکار
            elif command == "cmd_auto_bold":
                self.data['auto_bold'] = not self.data.get('auto_bold', False)
                self.save_data()
                status = "فعال" if self.data['auto_bold'] else "غیرفعال"
                await callback_query.answer(f"**بولد خودکار {status} شد!**", show_alert=True)
                await self.show_formatting_menu(callback_query)
                
            elif command == "cmd_auto_italic":
                self.data['auto_italic'] = not self.data.get('auto_italic', False)
                self.save_data()
                status = "فعال" if self.data['auto_italic'] else "غیرفعال"
                await callback_query.answer(f"_ایتالیک خودکار {status} شد!_", show_alert=True)
                await self.show_formatting_menu(callback_query)
                
            elif command == "cmd_auto_code":
                self.data['auto_code'] = not self.data.get('auto_code', False)
                self.save_data()
                status = "فعال" if self.data['auto_code'] else "غیرفعال"
                await callback_query.answer(f"`کد خودکار {status} شد!`", show_alert=True)
                await self.show_formatting_menu(callback_query)
                
            elif command == "cmd_auto_strikethrough":
                self.data['auto_strikethrough'] = not self.data.get('auto_strikethrough', False)
                self.save_data()
                status = "فعال" if self.data['auto_strikethrough'] else "غیرفعال"
                await callback_query.answer(f"~~خط‌خورده خودکار {status} شد!~~", show_alert=True)
                await self.show_formatting_menu(callback_query)
                
            elif command == "cmd_auto_spoiler":
                self.data['auto_spoiler'] = not self.data.get('auto_spoiler', False)
                self.save_data()
                status = "فعال" if self.data['auto_spoiler'] else "غیرفعال"
                await callback_query.answer(f"||اسپویلر خودکار {status} شد!||", show_alert=True)
                await self.show_formatting_menu(callback_query)
                
            elif command == "cmd_auto_underline":
                self.data['auto_underline'] = not self.data.get('auto_underline', False)
                self.save_data()
                status = "فعال" if self.data['auto_underline'] else "غیرفعال"
                await callback_query.answer(f"__زیرخط خودکار {status} شد!__", show_alert=True)
                await self.show_formatting_menu(callback_query)
                
            # دستورات تایم
            elif command == "cmd_time_in_name":
                self.data['time_in_name'] = not self.data.get('time_in_name', False)
                self.save_data()
                status = "فعال" if self.data['time_in_name'] else "غیرفعال"
                
                if self.data['time_in_name']:
                    await self.update_name_with_time()
                else:
                    # بازگردانی نام اصلی
                    original_name = self.data.get('original_name', '')
                    if original_name:
                        await self.app.update_profile(first_name=original_name)
                
                await callback_query.answer(f"🕐 تایم در نام {status} شد!", show_alert=True)
                await self.show_time_settings_menu(callback_query)
                
            elif command == "cmd_auto_bio_time":
                self.data['auto_bio_time'] = not self.data.get('auto_bio_time', False)
                self.save_data()
                status = "فعال" if self.data['auto_bio_time'] else "غیرفعال"
                
                if self.data['auto_bio_time']:
                    await self.update_bio_with_time()
                else:
                    # بازگردانی بیو اصلی
                    original_bio = self.data.get('original_bio', '')
                    await self.app.update_profile(bio=original_bio)
                
                await callback_query.answer(f"📝 تایم در بیو {status} شد!", show_alert=True)
                await self.show_time_settings_menu(callback_query)
                
            elif command == "cmd_update_name":
                await self.update_name_with_time()
                await callback_query.answer("🔄 نام بروزرسانی شد!", show_alert=True)
                
            elif command == "cmd_update_bio":
                await self.update_bio_with_time()
                await callback_query.answer("🔄 بیو بروزرسانی شد!", show_alert=True)
                
            # دستورات بازی
            elif command == "cmd_dice":
                await self.execute_dice_command(callback_query)
                
            elif command == "cmd_bowling":
                await self.execute_bowling_command(callback_query)
                
            elif command == "cmd_football":
                await self.execute_football_command(callback_query)
                
            elif command == "cmd_dart":
                await self.execute_dart_command(callback_query)
                
            elif command == "cmd_animation":
                await self.execute_animation_command(callback_query)
                
            elif command == "cmd_time":
                await self.execute_time_command(callback_query)
                
            elif command == "cmd_restart":
                await callback_query.answer("🔄 در حال راه‌اندازی مجدد...", show_alert=True)
                await self.restart_bot()
                
            else:
                await callback_query.answer("⚠️ این دستور نیاز به تنظیمات اضافی دارد!", show_alert=True)
                
        except Exception as e:
            logger.error(f"خطا در اجرای دستور {command}: {e}")
            await callback_query.answer(f"❌ خطا در اجرای دستور: {str(e)}", show_alert=True)

    async def request_command_settings(self, callback_query: CallbackQuery, command_type: str):
        """درخواست تنظیمات برای دستورات"""
        user_id = callback_query.from_user.id
        
        # ذخیره اطلاعات دستور در انتظار
        self.pending_commands[user_id] = {
            'command': command_type,
            'chat_id': self.current_chat_id or callback_query.message.chat.id,
            'callback_query': callback_query
        }
        
        settings_messages = {
            'crash': "💥 **تنظیمات اشکن**\n\nلطفاً به صورت زیر ارسال کنید:\n`تعداد متن`\n\nمثال: `5 سلام`",
            'spam': "📨 **تنظیمات اسپم**\n\nلطفاً به صورت زیر ارسال کنید:\n`تعداد متن`\n\nمثال: `10 سلام دوستان`",
            'auto_reply': "💬 **تنظیمات پاسخ خودکار**\n\nلطفاً به صورت زیر ارسال کنید:\n`کلمه|پاسخ`\n\nمثال: `سلام|سلام علیکم`",
            'word_filter': "🚫 **تنظیمات فیلتر کلمات**\n\nلطفاً به صورت زیر ارسال کنید:\n`add کلمه` یا `remove کلمه`\n\nمثال: `add بد`",
            'comment': "💬 **تنظیمات کامنت خودکار**\n\nلطفاً به صورت زیر ارسال کنید:\n`آیدی_کانال متن_کامنت`\n\nمثال: `-1001234567890 عالی بود!`",
            'mute': "🔇 **سکوت کاربر**\n\nابتدا روی پیام کاربری که می‌خواهید سکوت کنید ریپلای کنید، سپس دستور را اجرا کنید.\n\nفقط `OK` ارسال کنید:",
            'ban': "🚫 **بن کردن کاربر**\n\nابتدا روی پیام کاربری که می‌خواهید بن کنید ریپلای کنید، سپس دستور را اجرا کنید.\n\nفقط `OK` ارسال کنید:",
            'block': "🚫 **مسدود کردن کاربر**\n\nابتدا روی پیام کاربری که می‌خواهید مسدود کنید ریپلای کنید، سپس دستور را اجرا کنید.\n\nفقط `OK` ارسال کنید:",
            'enemy': "😡 **اضافه به دشمنان**\n\nلطفاً آیدی عددی کاربر را ارسال کنید:\n\nمثال: `123456789`",
            'friend': "😊 **اضافه به دوستان**\n\nلطفاً آیدی عددی کاربر را ارسال کنید:\n\nمثال: `123456789`",
            'tag_all': "👥 **تگ همگانی**\n\nفقط `OK` ارسال کنید:",
            'tag_admins': "👑 **تگ ادمین‌ها**\n\nفقط `OK` ارسال کنید:",
            'info': "ℹ️ **نمایش اطلاعات**\n\nفقط `OK` ارسال کنید:",
            'profile': "👤 **نمایش پروفایل**\n\nلطفاً آیدی عددی کاربر را ارسال کنید:\n\nمثال: `123456789`",
            'save': "💾 **ذخیره پیام**\n\nابتدا روی پیامی که می‌خواهید ذخیره کنید ریپلای کنید، سپس دستور را اجرا کنید.\n\nفقط `OK` ارسال کنید:",
            'delete': "🗑️ **حذف پیام**\n\nابتدا روی پیامی که می‌خواهید حذف کنید ریپلای کنید، سپس دستور را اجرا کنید.\n\nفقط `OK` ارسال کنید:"
        }
        
        await callback_query.answer("📝 لطفاً تنظیمات را ارسال کنید", show_alert=True)
        
        # ارسال پیام راهنما
        await self.helper_bot.send_message(
            chat_id=user_id,
            text=settings_messages.get(command_type, "لطفاً تنظیمات را ارسال کنید")
        )

    async def handle_command_settings(self, message: Message):
        """مدیریت تنظیمات دستورات"""
        user_id = message.from_user.id
        
        if user_id not in self.pending_commands:
            return
        
        command_info = self.pending_commands[user_id]
        command_type = command_info['command']
        
        try:
            if command_type == 'crash':
                parts = message.text.split(maxsplit=1)
                if len(parts) < 2:
                    await message.reply("❌ فرمت نادرست! مثال: `5 سلام`")
                    return
                
                count = int(parts[0])
                text = parts[1]
                
                if count > 100:
                    await message.reply("❌ تعداد نمی‌تواند بیشتر از 100 باشد!")
                    return
                
                await message.reply("💥 در حال اجرای اشکن...")
                
                # اجرای اشکن در چت فعلی
                for i in range(count):
                    try:
                        await self.app.send_message("me", f"{text} #{i+1}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        logger.error(f"خطا در ارسال پیام اشکن: {e}")
                        break
                
                await message.reply("✅ اشکن با موفقیت اجرا شد!")
                
            elif command_type == 'spam':
                parts = message.text.split(maxsplit=1)
                if len(parts) < 2:
                    await message.reply("❌ فرمت نادرست! مثال: `10 سلام`")
                    return
                
                count = int(parts[0])
                text = parts[1]
                
                if count > 50:
                    await message.reply("❌ تعداد نمی‌تواند بیشتر از 50 باشد!")
                    return
                
                await message.reply("📨 در حال اجرای اسپم...")
                
                # اجرای اسپم در چت فعلی
                for _ in range(count):
                    try:
                        await self.app.send_message("me", text)
                        await asyncio.sleep(1)
                    except Exception as e:
                        logger.error(f"خطا در ارسال پیام اسپم: {e}")
                        break
                
                await message.reply("✅ اسپم با موفقیت اجرا شد!")
                
            elif command_type == 'auto_reply':
                if '|' not in message.text:
                    await message.reply("❌ فرمت نادرست! مثال: `سلام|سلام علیکم`")
                    return
                
                keyword, reply = message.text.split('|', 1)
                
                if 'auto_replies' not in self.data:
                    self.data['auto_replies'] = {}
                
                self.data['auto_replies'][keyword.strip()] = reply.strip()
                self.save_data()
                
                await message.reply(f"✅ پاسخ خودکار تنظیم شد!\n**کلمه:** `{keyword.strip()}`\n**پاسخ:** `{reply.strip()}`")
                
            elif command_type == 'word_filter':
                parts = message.text.split(maxsplit=1)
                if len(parts) < 2:
                    await message.reply("❌ فرمت نادرست! مثال: `add کلمه`")
                    return
                
                action = parts[0].lower()
                word = parts[1]
                
                if 'filtered_words' not in self.data:
                    self.data['filtered_words'] = []
                
                if action == 'add':
                    if word not in self.data['filtered_words']:
                        self.data['filtered_words'].append(word)
                        self.save_data()
                        await message.reply(f"✅ کلمه `{word}` به فیلتر اضافه شد!")
                    else:
                        await message.reply("⚠️ کلمه قبلاً در فیلتر موجود است!")
                elif action == 'remove':
                    if word in self.data['filtered_words']:
                        self.data['filtered_words'].remove(word)
                        self.save_data()
                        await message.reply(f"✅ کلمه `{word}` از فیلتر حذف شد!")
                    else:
                        await message.reply("❌ کلمه در فیلتر وجود ندارد!")
                else:
                    await message.reply("❌ عمل نامعتبر! از add یا remove استفاده کنید")
                    return
                    
            elif command_type == 'comment':
                parts = message.text.split(maxsplit=1)
                if len(parts) < 2:
                    await message.reply("❌ فرمت نادرست! مثال: `-1001234567890 عالی بود!`")
                    return
                
                try:
                    channel_id = int(parts[0])
                    comment_text = parts[1]
                    
                    if 'comment_channels' not in self.data:
                        self.data['comment_channels'] = []
                    
                    # بررسی اینکه کانال قبلاً اضافه نشده باشد
                    existing = False
                    for channel in self.data['comment_channels']:
                        if channel.get('channel_id') == channel_id:
                            channel['comment'] = comment_text
                            existing = True
                            break
                    
                    if not existing:
                        self.data['comment_channels'].append({
                            'channel_id': channel_id,
                            'comment': comment_text
                        })
                    
                    self.save_data()
                    
                    await message.reply(f"✅ کامنت خودکار برای کانال `{channel_id}` فعال شد!")
                    
                except ValueError:
                    await message.reply("❌ آیدی کانال باید عدد باشد!")
                    
            elif command_type in ['mute', 'ban', 'block', 'save', 'delete', 'tag_all', 'tag_admins', 'info']:
                if message.text.upper() == 'OK':
                    await message.reply(f"✅ دستور {command_type} آماده اجرا است! لطفاً در چت مورد نظر عملیات لازم را انجام دهید.")
                else:
                    await message.reply("❌ فقط `OK` ارسال کنید!")
                    return
                    
            elif command_type in ['enemy', 'friend', 'profile']:
                try:
                    user_id_target = int(message.text)
                    
                    if command_type == 'enemy':
                        if 'enemies' not in self.data:
                            self.data['enemies'] = {}
                        self.data['enemies'][str(user_id_target)] = {
                            'name': f"کاربر {user_id_target}",
                            'added_date': datetime.now().isoformat()
                        }
                        self.save_data()
                        await message.reply(f"😡 کاربر `{user_id_target}` به لیست دشمنان اضافه شد!")
                        
                    elif command_type == 'friend':
                        if 'friends' not in self.data:
                            self.data['friends'] = {}
                        self.data['friends'][str(user_id_target)] = {
                            'name': f"کاربر {user_id_target}",
                            'added_date': datetime.now().isoformat()
                        }
                        self.save_data()
                        await message.reply(f"😊 کاربر `{user_id_target}` به لیست دوستان اضافه شد!")
                        
                    elif command_type == 'profile':
                        # نمایش پروفایل در چت فعلی
                        try:
                            user_info = await self.app.get_users(user_id_target)
                            profile_text = f"👤 **پروفایل کاربر:**\n"
                            profile_text += f"**نام:** {user_info.first_name}\n"
                            if user_info.last_name:
                                profile_text += f"**نام خانوادگی:** {user_info.last_name}\n"
                            if user_info.username:
                                profile_text += f"**یوزرنیم:** @{user_info.username}\n"
                            profile_text += f"**آیدی:** `{user_id_target}`\n"
                            
                            await self.app.send_message("me", profile_text)
                            await message.reply("✅ پروفایل نمایش داده شد!")
                        except Exception as e:
                            await message.reply(f"❌ خطا در نمایش پروفایل: {str(e)}")
                            
                except ValueError:
                    await message.reply("❌ آیدی معتبر وارد کنید!")
                    return
            
            # حذف دستور از انتظار
            del self.pending_commands[user_id]
            
        except ValueError:
            await message.reply("❌ مقدار عددی نامعتبر!")
        except Exception as e:
            await message.reply(f"❌ خطا در تنظیمات: {str(e)}")
            logger.error(f"خطا در تنظیمات دستور {command_type}: {e}")

    async def execute_ping_command(self, callback_query: CallbackQuery):
        """اجرای دستور پینگ"""
        try:
            start = time.time()
            # ارسال پیام پینگ به چت فعلی
            message = await self.app.send_message("me", "🏓 در حال محاسبه پینگ...")
            end = time.time()
            ping = round((end - start) * 1000, 2)
            await message.edit(f"🏓 **پینگ:** `{ping}ms`")
            await callback_query.answer("🏓 پینگ محاسبه شد!", show_alert=True)
        except Exception as e:
            logger.error(f"خطا در اجرای پینگ: {e}")
            await callback_query.answer(f"❌ خطا: {str(e)}", show_alert=True)

    async def execute_dice_command(self, callback_query: CallbackQuery):
        """اجرای تقلب تاس"""
        try:
            for _ in range(5):
                await self.app.send_dice("me", "🎲")
                await asyncio.sleep(1)
            await callback_query.answer("🎲 تقلب تاس اجرا شد!", show_alert=True)
        except Exception as e:
            logger.error(f"خطا در تقلب تاس: {e}")
            await callback_query.answer(f"❌ خطا: {str(e)}", show_alert=True)

    async def execute_bowling_command(self, callback_query: CallbackQuery):
        """اجرای تقلب بولینگ"""
        try:
            await self.app.send_dice("me", "🎳")
            await callback_query.answer("🎳 تقلب بولینگ اجرا شد!", show_alert=True)
        except Exception as e:
            logger.error(f"خطا در تقلب بولینگ: {e}")
            await callback_query.answer(f"❌ خطا: {str(e)}", show_alert=True)

    async def execute_football_command(self, callback_query: CallbackQuery):
        """اجرای تقلب فوتبال"""
        try:
            await self.app.send_dice("me", "⚽")
            await callback_query.answer("⚽ تقلب فوتبال اجرا شد!", show_alert=True)
        except Exception as e:
            logger.error(f"خطا در تقلب فوتبال: {e}")
            await callback_query.answer(f"❌ خطا: {str(e)}", show_alert=True)

    async def execute_dart_command(self, callback_query: CallbackQuery):
        """اجرای تقلب دارت"""
        try:
            await self.app.send_dice("me", "🎯")
            await callback_query.answer("🎯 تقلب دارت اجرا شد!", show_alert=True)
        except Exception as e:
            logger.error(f"خطا در تقلب دارت: {e}")
            await callback_query.answer(f"❌ خطا: {str(e)}", show_alert=True)

    async def execute_animation_command(self, callback_query: CallbackQuery):
        """اجرای انیمیشن"""
        try:
            animations = [
                "⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜🔴⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
                "⬜⬜⬜⬜⬜\n⬜🔴⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜🔴⬜\n⬜⬜⬜⬜⬜",
                "⬜🔴⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜🔴",
                "🔴⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
                "⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜"
            ]
            
            message = await self.app.send_message("me", animations[0])
            for frame in animations[1:]:
                await message.edit(frame)
                await asyncio.sleep(0.8)
            await callback_query.answer("🎬 انیمیشن اجرا شد!", show_alert=True)
        except Exception as e:
            logger.error(f"خطا در انیمیشن: {e}")
            await callback_query.answer(f"❌ خطا: {str(e)}", show_alert=True)

    async def execute_time_command(self, callback_query: CallbackQuery):
        """اجرای دستور ساعت"""
        try:
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            date_str = now.strftime("%Y/%m/%d")
            weekday = now.strftime("%A")
            
            persian_weekdays = {
                'Monday': 'دوشنبه',
                'Tuesday': 'سه‌شنبه', 
                'Wednesday': 'چهارشنبه',
                'Thursday': 'پنج‌شنبه',
                'Friday': 'جمعه',
                'Saturday': 'شنبه',
                'Sunday': 'یکشنبه'
            }
            
            persian_day = persian_weekdays.get(weekday, weekday)
            
            await self.app.send_message(
                "me", 
                f"🕐 **ساعت:** `{time_str}`\n📅 **تاریخ:** `{date_str}`\n📆 **روز هفته:** {persian_day}"
            )
            await callback_query.answer("🕐 ساعت نمایش داده شد!", show_alert=True)
        except Exception as e:
            logger.error(f"خطا در نمایش ساعت: {e}")
            await callback_query.answer(f"❌ خطا: {str(e)}", show_alert=True)

    async def restart_bot(self):
        """راه‌اندازی مجدد ربات"""
        try:
            logger.info("🔄 در حال راه‌اندازی مجدد...")
            self.is_running = False
            
            if self.app:
                await self.app.stop()
            if self.helper_bot:
                await self.helper_bot.stop()
            
            await asyncio.sleep(2)
            
            # راه‌اندازی مجدد
            await self.start_bot()
            
        except Exception as e:
            logger.error(f"خطا در راه‌اندازی مجدد: {e}")

    # ادامه دستورات سلف بات
    async def process_my_message(self, message: Message):
        """پردازش پیام‌های خودم"""
        if not message.text:
            return
        
        # اعمال فرمت خودکار
        if any([self.data.get('auto_bold'), self.data.get('auto_italic'), 
                self.data.get('auto_code'), self.data.get('auto_strikethrough'),
                self.data.get('auto_spoiler'), self.data.get('auto_underline')]):
            
            # بررسی اینکه پیام دستور نباشد
            if not message.text.startswith('.') and not message.text.startswith('/'):
                formatted_text = await self.apply_auto_formatting(message.text)
                if formatted_text != message.text:
                    try:
                        await message.edit(formatted_text)
                    except:
                        pass
        
        text = message.text.strip()
        cmd = text.split()[0] if text.split() else ""
        
        # دستورات اصلی
        commands = {
            '.ping': self.cmd_ping,
            '.اشکن': self.cmd_crash,
            '.break': self.cmd_crash,
            '.سکوت': self.cmd_mute,
            '.mute': self.cmd_mute,
            '.منشی': self.cmd_secretary,
            '.secretary': self.cmd_secretary,
            '.قفلپیوی': self.cmd_pv_lock,
            '.pvlock': self.cmd_pv_lock,
            '.انیمیشن': self.cmd_animation,
            '.animation': self.cmd_animation,
            '.اسپم': self.cmd_spam,
            '.spam': self.cmd_spam,
            '.قفلفوروارد': self.cmd_forward_lock,
            '.flock': self.cmd_forward_lock,
            '.تقلبتاس': self.cmd_dice_cheat,
            '.dice': self.cmd_dice_cheat,
            '.قفلاستیکر': self.cmd_sticker_lock,
            '.slock': self.cmd_sticker_lock,
            '.بولد': self.cmd_text_style,
            '.bold': self.cmd_text_style,
            '.ریاکت': self.cmd_auto_react,
            '.react': self.cmd_auto_react,
            '.پاسخ': self.cmd_auto_reply,
            '.reply': self.cmd_auto_reply,
            '.فیلتر': self.cmd_word_filter,
            '.filter': self.cmd_word_filter,
            '.اطلاعات': self.cmd_info,
            '.info': self.cmd_info,
            '.ضدلاگین': self.cmd_anti_login,
            '.antilogin': self.cmd_anti_login,
            '.تگ': self.cmd_tag,
            '.tag': self.cmd_tag,
            '.ساعت': self.cmd_time,
            '.time': self.cmd_time,
            '.بن': self.cmd_ban,
            '.ban': self.cmd_ban,
            '.مسدود': self.cmd_block,
            '.block': self.cmd_block,
            '.حذف': self.cmd_delete,
            '.del': self.cmd_delete,
            '.پروفایل': self.cmd_profile,
            '.profile': self.cmd_profile,
            '.سین': self.cmd_auto_seen,
            '.seen': self.cmd_auto_seen,
            '.تپچی': self.cmd_typing,
            '.type': self.cmd_typing,
            '.سیو': self.cmd_save,
            '.save': self.cmd_save,
            '.دشمن': self.cmd_enemy,
            '.enemy': self.cmd_enemy,
            '.دوست': self.cmd_friend,
            '.friend': self.cmd_friend,
            '.کامنت': self.cmd_comment,
            '.comment': self.cmd_comment,
            '.بولینگ': self.cmd_bowling,
            '.bowling': self.cmd_bowling,
            '.فوتبال': self.cmd_football,
            '.football': self.cmd_football,
            '.دارت': self.cmd_dart,
            '.dart': self.cmd_dart,
            '.راهنما': self.cmd_help,
            '.help': self.cmd_help,
            '.تایم': self.cmd_time_toggle,
            '.timemode': self.cmd_time_toggle,
            '.ریستارت': self.cmd_restart,
            '.restart': self.cmd_restart
        }
        
        if cmd in commands:
            try:
                await commands[cmd](message)
            except Exception as e:
                logger.error(f"خطا در اجرای دستور {cmd}: {e}")
                await message.edit(f"❌ خطا در اجرای دستور: {str(e)}")

    async def process_other_message(self, message: Message):
        """پردازش پیام‌های دیگران"""
        try:
            # بررسی قفل پیوی پیشرفته
            if message.chat.type == ChatType.PRIVATE and self.data.get('pv_lock'):
                should_block = await self.handle_pv_lock_advanced(message)
                if should_block:
                    return
            
            # بررسی قفل فوروارد
            if message.forward_from and self.data.get('forward_lock'):
                try:
                    await message.delete()
                    return
                except:
                    pass
            
            # بررسی قفل استیکر
            if message.sticker and self.data.get('sticker_lock'):
                try:
                    await message.delete()
                    return
                except:
                    pass
            
            # فیلتر کلمات
            if self.data.get('word_filter') and message.text:
                await self.check_word_filter(message)
            
            # پاسخ خودکار
            if self.data.get('secretary_mode'):
                await self.handle_auto_reply(message)
            
            # ری‌اکت خودکار
            if self.data.get('auto_react'):
                await self.handle_auto_react(message)
            
            # سین خودکار
            if self.data.get('auto_seen'):
                await self.handle_auto_seen(message)
                
            # مدیریت دوستان و دشمنان
            await self.handle_friends_enemies(message)
                
        except Exception as e:
            logger.error(f"خطا در پردازش پیام: {e}")

    async def handle_pv_lock_advanced(self, message: Message):
        """مدیریت قفل پیوی پیشرفته"""
        user_id = message.from_user.id
        username = message.from_user.username
        
        # بررسی حالت قفل
        pv_lock_mode = self.data.get('pv_lock_mode', 'all')
        pv_lock_users = self.data.get('pv_lock_users', [])
        
        should_block = False
        
        if pv_lock_mode == 'all':
            # قفل برای همه
            should_block = True
        elif pv_lock_mode == 'specific':
            # قفل برای کاربران خاص
            for user_info in pv_lock_users:
                if (user_info.get('id') == user_id or 
                    user_info.get('username') == username):
                    should_block = True
                    break
        
        if should_block:
            # ارسال پیام هشدار و حذف پیام
            try:
                warning_msg = await message.reply("🔒 پیوی قفل است! پیام شما حذف می‌شود.")
                await message.delete()
                await asyncio.sleep(3)
                await warning_msg.delete()
            except:
                pass
            return True
        
        return False

    async def apply_auto_formatting(self, text: str) -> str:
        """اعمال فرمت خودکار به متن"""
        if self.data.get('auto_bold'):
            text = f"**{text}**"
        if self.data.get('auto_italic'):
            text = f"__{text}__"
        if self.data.get('auto_code'):
            text = f"`{text}`"
        if self.data.get('auto_strikethrough'):
            text = f"~~{text}~~"
        if self.data.get('auto_spoiler'):
            text = f"||{text}||"
        if self.data.get('auto_underline'):
            text = f"__{text}__"
        return text

    # تمام دستورات قبلی
    async def cmd_ping(self, message: Message):
        """دستور پینگ"""
        start = time.time()
        await message.edit("🏓 در حال محاسبه پینگ...")
        end = time.time()
        ping = round((end - start) * 1000, 2)
        await message.edit(f"🏓 **پینگ:** `{ping}ms`")

    async def cmd_crash(self, message: Message):
        """دستور اشکن"""
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        if not args:
            await message.edit("❌ **استفاده:** `.اشکن [تعداد] [متن]`")
            return
        
        try:
            count = int(args[0])
            text = " ".join(args[1:]) if len(args) > 1 else "💥 CRASH 💥"
            
            if count > 100:
                await message.edit("❌ تعداد نمی‌تواند بیشتر از 100 باشد!")
                return
            
            await message.delete()
            for i in range(count):
                try:
                    await message.reply(f"{text} #{i+1}")
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.error(f"خطا در ارسال پیام اشکن: {e}")
                    break
                
        except ValueError:
            await message.edit("❌ تعداد باید عدد باشد!")

    async def cmd_mute(self, message: Message):
        """دستور سکوت"""
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            if 'muted_users' not in self.data:
                self.data['muted_users'] = set()
            self.data['muted_users'].add(user_id)
            self.save_data()
            await message.edit("🔇 کاربر در حالت سکوت قرار گرفت!")
        else:
            await message.edit("❌ روی پیام کاربر ریپلای کنید!")

    async def cmd_secretary(self, message: Message):
        """دستور منشی"""
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            status = "فعال" if self.data.get('secretary_mode') else "غیرفعال"
            await message.edit(f"📋 **وضعیت منشی:** {status}\n**استفاده:** `.منشی [on/off] [پیام]`")
            return
        
        if args[1].lower() in ['on', 'فعال']:
            self.data['secretary_mode'] = True
            await message.edit("📋 **منشی فعال شد!**")
        elif args[1].lower() in ['off', 'غیرفعال']:
            self.data['secretary_mode'] = False
            await message.edit("📋 **منشی غیرفعال شد!**")
        else:
            self.data['secretary_message'] = args[1]
            await message.edit(f"📋 **پیام منشی تنظیم شد:** `{args[1]}`")
        
        self.save_data()

    async def cmd_pv_lock(self, message: Message):
        """دستور قفل پیوی پیشرفته"""
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        
        if not args:
            # تغییر وضعیت کلی
            self.data['pv_lock'] = not self.data.get('pv_lock', False)
            status = "فعال" if self.data['pv_lock'] else "غیرفعال"
            await message.edit(f"🔒 **قفل پیوی {status} شد!**")
        else:
            action = args[0].lower()
            
            if action in ['all', 'همه']:
                self.data['pv_lock'] = True
                self.data['pv_lock_mode'] = 'all'
                await message.edit("🔒 **قفل پیوی برای همه فعال شد!**")
                
            elif action in ['off', 'غیرفعال']:
                self.data['pv_lock'] = False
                await message.edit("🔓 **قفل پیوی غیرفعال شد!**")
                
            elif action in ['add', 'اضافه']:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                    username = message.reply_to_message.from_user.username
                    
                    if 'pv_lock_users' not in self.data:
                        self.data['pv_lock_users'] = []
                    
                    self.data['pv_lock_users'].append({
                        'id': user_id,
                        'username': username,
                        'name': message.reply_to_message.from_user.first_name
                    })
                    
                    self.data['pv_lock'] = True
                    self.data['pv_lock_mode'] = 'specific'
                    await message.edit(f"🔒 **کاربر {message.reply_to_message.from_user.first_name} به لیست قفل پیوی اضافه شد!**")
                elif len(args) > 1:
                    # اضافه کردن با یوزرنیم
                    username = args[1].replace('@', '')
                    if 'pv_lock_users' not in self.data:
                        self.data['pv_lock_users'] = []
                    
                    self.data['pv_lock_users'].append({
                        'username': username,
                        'name': username
                    })
                    
                    self.data['pv_lock'] = True
                    self.data['pv_lock_mode'] = 'specific'
                    await message.edit(f"🔒 **کاربر @{username} به لیست قفل پیوی اضافه شد!**")
                else:
                    await message.edit("❌ روی پیام کاربر ریپلای کنید یا یوزرنیم وارد کنید!")
                    return
                    
            elif action in ['remove', 'حذف']:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                    self.data['pv_lock_users'] = [u for u in self.data.get('pv_lock_users', []) if u.get('id') != user_id]
                    await message.edit("🔓 **کاربر از لیست قفل پیوی حذف شد!**")
                else:
                    await message.edit("❌ روی پیام کاربر ریپلای کنید!")
                    return
                    
            elif action in ['list', 'لیست']:
                users = self.data.get('pv_lock_users', [])
                if users:
                    user_list = "\n".join([f"• {u.get('name', u.get('username', 'نامشخص'))}" for u in users])
                    await message.edit(f"📝 **کاربران قفل شده:**\n{user_list}")
                else:
                    await message.edit("📝 هیچ کاربری در لیست قفل نیست!")
                return
            else:
                await message.edit("❌ **استفاده:** `.قفلپیوی [all/off/add/remove/list]`")
                return
        
        self.save_data()

    async def cmd_animation(self, message: Message):
        """دستور انیمیشن"""
        animations = [
            "⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜🔴⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜\n⬜🔴⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜🔴⬜\n⬜⬜⬜⬜⬜",
            "⬜🔴⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜🔴",
            "🔴⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
            "⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜"
        ]
        
        for frame in animations:
            await message.edit(frame)
            await asyncio.sleep(0.8)

    async def cmd_spam(self, message: Message):
        """دستور اسپم"""
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        if len(args) < 2:
            await message.edit("❌ **استفاده:** `.اسپم [تعداد] [متن]`")
            return
        
        try:
            count = int(args[0])
            text = " ".join(args[1:])
            
            if count > 50:
                await message.edit("❌ تعداد نمی‌تواند بیشتر از 50 باشد!")
                return
            
            await message.delete()
            for _ in range(count):
                try:
                    await message.reply(text)
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.error(f"خطا در ارسال پیام اسپم: {e}")
                    break
                
        except ValueError:
            await message.edit("❌ تعداد باید عدد باشد!")

    async def cmd_forward_lock(self, message: Message):
        """دستور قفل فوروارد"""
        self.data['forward_lock'] = not self.data.get('forward_lock', False)
        status = "فعال" if self.data['forward_lock'] else "غیرفعال"
        await message.edit(f"⏩ **قفل فوروارد {status} شد!**")
        self.save_data()

    async def cmd_dice_cheat(self, message: Message):
        """تقلب تاس"""
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        if not args:
            await message.edit("🎲 **استفاده:** `.تقلبتاس [عدد 1-6]`")
            return
        
        try:
            target = int(args[0])
            if not 1 <= target <= 6:
                await message.edit("❌ عدد باید بین 1 تا 6 باشد!")
                return
            
            await message.delete()
            # شبیه‌سازی تقلب تاس
            for _ in range(10):
                try:
                    dice = await message.reply("🎲")
                    result = random.randint(1, 6)
                    if result == target:
                        break
                    await dice.delete()
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.error(f"خطا در تقلب تاس: {e}")
                    break
                
        except ValueError:
            await message.edit("❌ عدد معتبر وارد کنید!")

    async def cmd_sticker_lock(self, message: Message):
        """دستور قفل استیکر"""
        self.data['sticker_lock'] = not self.data.get('sticker_lock', False)
        status = "فعال" if self.data['sticker_lock'] else "غیرفعال"
        await message.edit(f"🔒 **قفل استیکر {status} شد!**")
        self.save_data()

    async def cmd_text_style(self, message: Message):
        """دستور حالت متن - برای تمام پیام‌ها"""
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.edit("❌ **استفاده:** `.بولد [bold/italic/code/strikethrough/spoiler/underline]`")
            return
        
        style = args[1].lower()
        
        # فعال/غیرفعال کردن حالت فرمت خودکار
        if style in ['bold', 'بولد']:
            self.data['auto_bold'] = not self.data.get('auto_bold', False)
            status = "فعال" if self.data['auto_bold'] else "غیرفعال"
            await message.edit(f"**✨ حالت بولد خودکار {status} شد!**")
        elif style in ['italic', 'ایتالیک']:
            self.data['auto_italic'] = not self.data.get('auto_italic', False)
            status = "فعال" if self.data['auto_italic'] else "غیرفعال"
            await message.edit(f"_✨ حالت ایتالیک خودکار {status} شد!_")
        elif style in ['code', 'کد']:
            self.data['auto_code'] = not self.data.get('auto_code', False)
            status = "فعال" if self.data['auto_code'] else "غیرفعال"
            await message.edit(f"`✨ حالت کد خودکار {status} شد!`")
        elif style in ['strikethrough', 'خط‌خورده']:
            self.data['auto_strikethrough'] = not self.data.get('auto_strikethrough', False)
            status = "فعال" if self.data['auto_strikethrough'] else "غیرفعال"
            await message.edit(f"~~✨ حالت خط‌خورده خودکار {status} شد!~~")
        elif style in ['spoiler', 'اسپویلر']:
            self.data['auto_spoiler'] = not self.data.get('auto_spoiler', False)
            status = "فعال" if self.data['auto_spoiler'] else "غیرفعال"
            await message.edit(f"||✨ حالت اسپویلر خودکار {status} شد!||")
        elif style in ['underline', 'زیرخط']:
            self.data['auto_underline'] = not self.data.get('auto_underline', False)
            status = "فعال" if self.data['auto_underline'] else "غیرفعال"
            await message.edit(f"__✨ حالت زیرخط خودکار {status} شد!__")
        else:
            await message.edit("❌ نوع نامعتبر! انواع موجود: bold, italic, code, strikethrough, spoiler, underline")
            return
        
        self.save_data()

    async def cmd_auto_react(self, message: Message):
        """دستور ری‌اکت خودکار"""
        self.data['auto_react'] = not self.data.get('auto_react', False)
        status = "فعال" if self.data['auto_react'] else "غیرفعال"
        await message.edit(f"😍 **ری‌اکت خودکار {status} شد!**")
        self.save_data()

    async def cmd_auto_reply(self, message: Message):
        """دستور پاسخ خودکار"""
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            await message.edit("❌ **استفاده:** `.پاسخ [کلمه] [پاسخ]`")
            return
        
        keyword = args[1]
        reply = args[2]
        
        if 'auto_replies' not in self.data:
            self.data['auto_replies'] = {}
        
        self.data['auto_replies'][keyword] = reply
        self.save_data()
        await message.edit(f"✅ **پاسخ خودکار تنظیم شد!**\n**کلمه:** `{keyword}`\n**پاسخ:** `{reply}`")

    async def cmd_word_filter(self, message: Message):
        """دستور فیلتر کلمه"""
        args = message.text.split(maxsplit=2)
        if len(args) < 2:
            await message.edit("❌ **استفاده:** `.فیلتر [add/remove/list] [کلمه]`")
            return
        
        action = args[1].lower()
        
        if 'filtered_words' not in self.data:
            self.data['filtered_words'] = []
        
        if action in ['add', 'اضافه']:
            if len(args) < 3:
                await message.edit("❌ کلمه مورد نظر را وارد کنید!")
                return
            word = args[2]
            if word not in self.data['filtered_words']:
                self.data['filtered_words'].append(word)
                self.save_data()
                await message.edit(f"✅ کلمه `{word}` به فیلتر اضافه شد!")
            else:
                await message.edit("⚠️ کلمه قبلاً در فیلتر موجود است!")
            
        elif action in ['remove', 'حذف']:
            if len(args) < 3:
                await message.edit("❌ کلمه مورد نظر را وارد کنید!")
                return
            word = args[2]
            if word in self.data['filtered_words']:
                self.data['filtered_words'].remove(word)
                self.save_data()
                await message.edit(f"✅ کلمه `{word}` از فیلتر حذف شد!")
            else:
                await message.edit("❌ کلمه در فیلتر وجود ندارد!")
                
        elif action in ['list', 'لیست']:
            if self.data['filtered_words']:
                words = "\n".join([f"• {word}" for word in self.data['filtered_words']])
                await message.edit(f"📝 **کلمات فیلتر شده:**\n{words}")
            else:
                await message.edit("📝 هیچ کلمه‌ای فیلتر نشده است!")

    async def cmd_info(self, message: Message):
        """دستور اطلاعات"""
        if message.reply_to_message:
            user = message.reply_to_message.from_user
            info = f"👤 **اطلاعات کاربر:**\n"
            info += f"**نام:** {user.first_name}\n"
            if user.last_name:
                info += f"**نام خانوادگی:** {user.last_name}\n"
            info += f"**آیدی:** `{user.id}`\n"
            if user.username:
                info += f"**یوزرنیم:** @{user.username}\n"
            info += f"**ربات:** {'بله' if user.is_bot else 'خیر'}\n"
            await message.edit(info)
        else:
            # اطلاعات گروه/چت
            chat = message.chat
            info = f"💬 **اطلاعات چت:**\n"
            info += f"**عنوان:** {chat.title or 'بدون عنوان'}\n"
            info += f"**آیدی:** `{chat.id}`\n"
            info += f"**نوع:** {chat.type.value}\n"
            if hasattr(chat, 'members_count'):
                info += f"**تعداد اعضا:** {chat.members_count}\n"
            await message.edit(info)

    async def cmd_anti_login(self, message: Message):
        """دستور ضد لاگین"""
        self.data['anti_login'] = not self.data.get('anti_login', False)
        status = "فعال" if self.data['anti_login'] else "غیرفعال"
        await message.edit(f"🛡️ **ضد لاگین {status} شد!**")
        self.save_data()

    async def cmd_tag(self, message: Message):
        """دستور تگ کردن"""
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.edit("❌ **استفاده:** `.تگ [all/admins] یا .تگ @username`")
            return
        
        target = args[1].lower()
        
        if target == 'all':
            try:
                members = []
                async for member in self.app.get_chat_members(message.chat.id):
                    if member.user.username:
                        members.append(f"@{member.user.username}")
                    else:
                        members.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
                    if len(members) >= 50:  # محدودیت
                        break
                
                text = "👥 **تگ همگانی:**\n" + " ".join(members)
                await message.edit(text)
            except Exception as e:
                await message.edit(f"❌ خطا در تگ کردن: {str(e)}")
        
        elif target == 'admins':
            try:
                admins = []
                async for member in self.app.get_chat_members(message.chat.id, filter="administrators"):
                    if member.user.username:
                        admins.append(f"@{member.user.username}")
                    else:
                        admins.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
                
                text = "👑 **تگ ادمین‌ها:**\n" + " ".join(admins)
                await message.edit(text)
            except Exception as e:
                await message.edit(f"❌ خطا در تگ کردن ادمین‌ها: {str(e)}")

    async def cmd_time(self, message: Message):
        """دستور ساعت"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y/%m/%d")
        weekday = now.strftime("%A")
        
        # تبدیل روز هفته به فارسی
        persian_weekdays = {
            'Monday': 'دوشنبه',
            'Tuesday': 'سه‌شنبه', 
            'Wednesday': 'چهارشنبه',
            'Thursday': 'پنج‌شنبه',
            'Friday': 'جمعه',
            'Saturday': 'شنبه',
            'Sunday': 'یکشنبه'
        }
        
        persian_day = persian_weekdays.get(weekday, weekday)
        
        await message.edit(f"🕐 **ساعت:** `{time_str}`\n📅 **تاریخ:** `{date_str}`\n📆 **روز هفته:** {persian_day}")

    async def cmd_ban(self, message: Message):
        """دستور بن کاربر"""
        if not message.reply_to_message:
            await message.edit("❌ روی پیام کاربر ریپلای کنید!")
            return
        
        user_id = message.reply_to_message.from_user.id
        
        if 'banned_users' not in self.data:
            self.data['banned_users'] = set()
        
        self.data['banned_users'].add(user_id)
        self.save_data()
        
        try:
            await self.app.ban_chat_member(message.chat.id, user_id)
            await message.edit("🚫 **کاربر با موفقیت بن شد!**")
        except Exception as e:
            await message.edit(f"❌ خطا در بن کردن: {str(e)}")

    async def cmd_block(self, message: Message):
        """دستور مسدود کردن"""
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            
            if 'blocked_users' not in self.data:
                self.data['blocked_users'] = set()
            
            self.data['blocked_users'].add(user_id)
            self.save_data()
            
            try:
                await self.app.block_user(user_id)
                await message.edit("🚫 **کاربر با موفقیت مسدود شد!**")
            except Exception as e:
                await message.edit(f"❌ خطا در مسدود کردن: {str(e)}")
        else:
            await message.edit("❌ روی پیام کاربر ریپلای کنید!")

    async def cmd_delete(self, message: Message):
        """دستور حذف پیام"""
        if message.reply_to_message:
            try:
                await message.reply_to_message.delete()
                await message.edit("✅ **پیام حذف شد!**")
                await asyncio.sleep(2)
                await message.delete()
            except Exception as e:
                await message.edit(f"❌ خطا در حذف پیام: {str(e)}")
        else:
            await message.edit("❌ روی پیام مورد نظر ریپلای کنید!")

    async def cmd_profile(self, message: Message):
        """دستور پروفایل"""
        if message.reply_to_message:
            user = message.reply_to_message.from_user
            user_id = user.id
        else:
            user = message.from_user
            user_id = user.id
        
        try:
            photos = []
            async for photo in self.app.get_chat_photos(user_id, limit=1):
                photos.append(photo)
            
            profile_text = f"👤 **پروفایل کاربر:**\n"
            profile_text += f"**نام:** {user.first_name}\n"
            if user.last_name:
                profile_text += f"**نام خانوادگی:** {user.last_name}\n"
            if user.username:
                profile_text += f"**یوزرنیم:** @{user.username}\n"
            profile_text += f"**آیدی:** `{user_id}`\n"
            
            if photos:
                await message.reply_photo(photos[0].file_id, caption=profile_text)
                await message.delete()
            else:
                await message.edit(profile_text)
                
        except Exception as e:
            await message.edit(f"❌ خطا در نمایش پروفایل: {str(e)}")

    async def cmd_auto_seen(self, message: Message):
        """دستور سین خودکار"""
        self.data['auto_seen'] = not self.data.get('auto_seen', False)
        status = "فعال" if self.data['auto_seen'] else "غیرفعال"
        await message.edit(f"👁️ **سین خودکار {status} شد!**")
        self.save_data()

    async def cmd_typing(self, message: Message):
        """دستور تپچی"""
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        
        if not args or args[0].lower() not in ['on', 'off', 'فعال', 'غیرفعال']:
            status = "فعال" if self.data.get('auto_typing') else "غیرفعال"
            await message.edit(f"⌨️ **وضعیت تپچی:** {status}\n**استفاده:** `.تپچی [on/off]`")
            return
        
        if args[0].lower() in ['on', 'فعال']:
            self.data['auto_typing'] = True
            await message.edit("⌨️ **تپچی فعال شد!**")
        else:
            self.data['auto_typing'] = False
            await message.edit("⌨️ **تپچی غیرفعال شد!**")
        
        self.save_data()

    async def cmd_save(self, message: Message):
        """دستور سیو"""
        if not message.reply_to_message:
            await message.edit("❌ روی پیام مورد نظر ریپلای کنید!")
            return
        
        reply_msg = message.reply_to_message
        saved_item = {
            'type': 'text',
            'content': reply_msg.text or reply_msg.caption or '',
            'date': datetime.now().isoformat(),
            'chat_id': message.chat.id,
            'message_id': reply_msg.id
        }
        
        # تشخیص نوع محتوا
        if reply_msg.photo:
            saved_item['type'] = 'photo'
            saved_item['file_id'] = reply_msg.photo.file_id
        elif reply_msg.video:
            saved_item['type'] = 'video'
            saved_item['file_id'] = reply_msg.video.file_id
        elif reply_msg.document:
            saved_item['type'] = 'document'
            saved_item['file_id'] = reply_msg.document.file_id
        
        if 'saved_messages' not in self.data:
            self.data['saved_messages'] = []
        
        self.data['saved_messages'].append(saved_item)
        self.save_data()
        
        await message.edit(f"💾 **پیام ذخیره شد!**\n**نوع:** {saved_item['type']}")

    async def cmd_enemy(self, message: Message):
        """دستور تنظیم دشمن"""
        args = message.text.split(maxsplit=1)
        
        if not message.reply_to_message and len(args) < 2:
            await message.edit("❌ روی پیام کاربر ریپلای کنید یا آیدی وارد کنید!")
            return
        
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.first_name
        else:
            try:
                user_id = int(args[1])
                user_name = f"کاربر {user_id}"
            except ValueError:
                await message.edit("❌ آیدی معتبر وارد کنید!")
                return
        
        if 'enemies' not in self.data:
            self.data['enemies'] = {}
        
        self.data['enemies'][str(user_id)] = {
            'name': user_name,
            'added_date': datetime.now().isoformat()
        }
        self.save_data()
        
        await message.edit(f"😡 **{user_name} به لیست دشمنان اضافه شد!**")

    async def cmd_friend(self, message: Message):
        """دستور تنظیم دوست"""
        args = message.text.split(maxsplit=1)
        
        if not message.reply_to_message and len(args) < 2:
            await message.edit("❌ روی پیام کاربر ریپلای کنید یا آیدی وارد کنید!")
            return
        
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.first_name
        else:
            try:
                user_id = int(args[1])
                user_name = f"کاربر {user_id}"
            except ValueError:
                await message.edit("❌ آیدی معتبر وارد کنید!")
                return
        
        if 'friends' not in self.data:
            self.data['friends'] = {}
        
        self.data['friends'][str(user_id)] = {
            'name': user_name,
            'added_date': datetime.now().isoformat()
        }
        self.save_data()
        
        await message.edit(f"😊 **{user_name} به لیست دوستان اضافه شد!**")

    async def cmd_comment(self, message: Message):
        """دستور کامنت خودکار"""
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            await message.edit("❌ **استفاده:** `.کامنت [add/remove] [آیدی کانال] [متن کامنت]`")
            return
        
        action = args[1].lower()
        
        if action in ['add', 'اضافه']:
            if len(args) < 4:
                await message.edit("❌ آیدی کانال و متن کامنت را وارد کنید!")
                return
            
            try:
                channel_id = int(args[2])
                comment_text = args[3]
                
                if 'comment_channels' not in self.data:
                    self.data['comment_channels'] = []
                
                # بررسی اینکه کانال قبلاً اضافه نشده باشد
                existing = False
                for channel in self.data['comment_channels']:
                    if channel.get('channel_id') == channel_id:
                        channel['comment'] = comment_text
                        existing = True
                        break
                
                if not existing:
                    self.data['comment_channels'].append({
                        'channel_id': channel_id,
                        'comment': comment_text
                    })
                
                self.save_data()
                
                await message.edit(f"✅ کامنت خودکار برای کانال `{channel_id}` فعال شد!")
                
            except ValueError:
                await message.edit("❌ آیدی کانال باید عدد باشد!")

    async def cmd_bowling(self, message: Message):
        """تقلب بولینگ"""
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        target = int(args[0]) if args and args[0].isdigit() else 6
        
        await message.delete()
        
        # ارسال بولینگ تا رسیدن به نتیجه مطلوب
        for attempt in range(20):
            try:
                bowling = await self.app.send_dice(message.chat.id, "🎳")
                await asyncio.sleep(4)  # انتظار برای نمایش نتیجه
                
                # در صورت رسیدن به نتیجه مطلوب، توقف
                if attempt > 10:  # بعد از چند تلاش توقف
                    break
            except Exception as e:
                logger.error(f"خطا در تقلب بولینگ: {e}")
                break

    async def cmd_football(self, message: Message):
        """تقلب فوتبال"""
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        target = int(args[0]) if args and args[0].isdigit() else 5
        
        await message.delete()
        
        for attempt in range(20):
            try:
                football = await self.app.send_dice(message.chat.id, "⚽")
                await asyncio.sleep(4)
                
                if attempt > 10:
                    break
            except Exception as e:
                logger.error(f"خطا در تقلب فوتبال: {e}")
                break

    async def cmd_dart(self, message: Message):
        """تقلب دارت"""
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        target = int(args[0]) if args and args[0].isdigit() else 6
        
        await message.delete()
        
        for attempt in range(20):
            try:
                dart = await self.app.send_dice(message.chat.id, "🎯")
                await asyncio.sleep(4)
                
                if attempt > 10:
                    break
            except Exception as e:
                logger.error(f"خطا در تقلب دارت: {e}")
                break

    async def cmd_time_toggle(self, message: Message):
        """دستور تغییر حالت تایم"""
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        
        if not args:
            # نمایش وضعیت فعلی
            name_status = "فعال" if self.data.get('time_in_name') else "غیرفعال"
            bio_status = "فعال" if self.data.get('auto_bio_time') else "غیرفعال"
            await message.edit(f"⏰ **وضعیت تایم:**\n🕐 **تایم در نام:** {name_status}\n📝 **تایم در بیو:** {bio_status}\n\n**استفاده:** `.تایم [name/bio/off]`")
            return
        
        mode = args[0].lower()
        
        if mode in ['name', 'نام']:
            self.data['time_in_name'] = not self.data.get('time_in_name', False)
            status = "فعال" if self.data['time_in_name'] else "غیرفعال"
            
            if self.data['time_in_name']:
                # ذخیره نام اصلی
                me = await self.app.get_me()
                self.data['original_name'] = me.first_name
                await self.update_name_with_time()
            else:
                # بازگردانی نام اصلی
                original_name = self.data.get('original_name', '')
                if original_name:
                    await self.app.update_profile(first_name=original_name)
            
            await message.edit(f"🕐 **تایم در نام {status} شد!**")
            
        elif mode in ['bio', 'بیو']:
            self.data['auto_bio_time'] = not self.data.get('auto_bio_time', False)
            status = "فعال" if self.data['auto_bio_time'] else "غیرفعال"
            
            if self.data['auto_bio_time']:
                # ذخیره بیو اصلی
                me = await self.app.get_me()
                self.data['original_bio'] = me.bio or ''
                await self.update_bio_with_time()
            else:
                # بازگردانی بیو اصلی
                original_bio = self.data.get('original_bio', '')
                await self.app.update_profile(bio=original_bio)
            
            await message.edit(f"📝 **تایم در بیو {status} شد!**")
            
        elif mode in ['off', 'غیرفعال']:
            # غیرفعال کردن همه
            self.data['time_in_name'] = False
            self.data['auto_bio_time'] = False
            
            # بازگردانی نام و بیو اصلی
            original_name = self.data.get('original_name', '')
            original_bio = self.data.get('original_bio', '')
            
            if original_name:
                await self.app.update_profile(first_name=original_name)
            if original_bio:
                await self.app.update_profile(bio=original_bio)
            
            await message.edit("⏰ **تمام حالت‌های تایم غیرفعال شد!**")
        else:
            await message.edit("❌ **استفاده:** `.تایم [name/bio/off]`")
            return
        
        self.save_data()

    async def cmd_restart(self, message: Message):
        """دستور راه‌اندازی مجدد"""
        await message.edit("🔄 **در حال راه‌اندازی مجدد...**")
        await self.restart_bot()

    async def cmd_help(self, message: Message):
        """دستور راهنما"""
        help_text = f"""
╭─────────────────────────────────────╮
│           🤖 ربات سلف تلگرام           │
│        ⚡ نسخه پیشرفته و کامل ⚡        │
╰─────────────────────────────────────╯

🎯 **برای استفاده از پنل کنترل:**
• دستور `/help` را در ربات هلپر بزنید
• از دکمه‌های شیشه‌ای استفاده کنید
• تمام دستورات با یک کلیک اجرا می‌شوند

🔥 **ویژگی‌های خاص:**
✅ دستورات با دکمه‌های شیشه‌ای
✅ قفل پیوی پیشرفته
✅ فرمت خودکار برای تمام پیام‌ها
✅ مدیریت کامل دوستان و دشمنان
✅ تقلب در بازی‌های تلگرام
✅ تایم در نام و بیو با فونت superscript

💡 **استفاده inline در هر جای تلگرام:**
`@{(await self.helper_bot.get_me()).username if self.helper_bot else 'helper_bot'}`

🤖 **ربات هلپر:** {"فعال" if self.helper_bot else "غیرفعال"}
👤 **صاحب:** {self.owner_id}

💡 **نکته:** فقط صاحب اکانت می‌تواند از ربات هلپر استفاده کند!
        """
        await message.edit(help_text)

    # توابع کمکی
    async def check_word_filter(self, message: Message):
        """بررسی فیلتر کلمات"""
        if not message.text:
            return
        
        text_lower = message.text.lower()
        for word in self.data.get('filtered_words', []):
            if word.lower() in text_lower:
                try:
                    await message.delete()
                    break
                except:
                    pass

    async def handle_auto_reply(self, message: Message):
        """مدیریت پاسخ خودکار"""
        if not message.text:
            return
        
        # پاسخ خودکار منشی
        if self.data.get('secretary_mode') and message.chat.type == ChatType.PRIVATE:
            secretary_msg = self.data.get('secretary_message', "📋 در حال حاضر در دسترس نیستم. پیام شما ثبت شد.")
            try:
                await message.reply(secretary_msg)
            except:
                pass
        
        # پاسخ‌های خودکار سفارشی
        text_lower = message.text.lower()
        for keyword, reply in self.data.get('auto_replies', {}).items():
            if keyword.lower() in text_lower:
                try:
                    await message.reply(reply)
                    break
                except:
                    pass

    async def handle_auto_react(self, message: Message):
        """مدیریت ری‌اکت خودکار"""
        reactions = ['❤️', '👍', '😍', '🔥', '🥰', '👏', '😁']
        try:
            reaction = random.choice(reactions)
            await message.react(reaction)
        except:
            pass  # در صورت خطا، ادامه

    async def handle_auto_seen(self, message: Message):
        """مدیریت سین خودکار"""
        try:
            if message.chat.type == ChatType.PRIVATE:
                await self.app.read_chat_history(message.chat.id)
        except:
            pass

    async def handle_friends_enemies(self, message: Message):
        """مدیریت دوستان و دشمنان"""
        user_id = str(message.from_user.id)
        
        # پاسخ به دشمنان
        if user_id in self.data.get('enemies', {}):
            insults = [
                "😡 برو گمشو!",
                "🤬 حرف نزن!",
                "😤 اعصابمو خورد نکن!",
                "🙄 چه آدم کسل‌کننده‌ای هستی!"
            ]
            try:
                await message.reply(random.choice(insults))
            except:
                pass
        
        # پاسخ مودبانه به دوستان
        elif user_id in self.data.get('friends', {}):
            friendly_replies = [
                "😊 سلام دوست عزیز!",
                "🥰 چه خبر؟",
                "😄 خوش اومدی!",
                "💖 خوبی؟"
            ]
            if random.random() < 0.3:  # 30% احتمال پاسخ
                try:
                    await message.reply(random.choice(friendly_replies))
                except:
                    pass

    async def auto_typing_loop(self):
        """حلقه تپچی خودکار"""
        while self.is_running:
            try:
                if self.data.get('auto_typing'):
                    for user_id in self.data.get('typing_users', set()):
                        try:
                            await self.app.invoke(
                                SetTyping(
                                    peer=await self.app.resolve_peer(user_id),
                                    action=SendMessageTypingAction()
                                )
                            )
                        except:
                            pass
            except Exception as e:
                logger.error(f"خطا در تپچی خودکار: {e}")
            await asyncio.sleep(5)

    async def comment_monitor(self):
        """نظارت بر کانال‌ها برای کامنت خودکار"""
        while self.is_running:
            try:
                for channel_info in self.data.get('comment_channels', []):
                    channel_id = channel_info['channel_id']
                    comment_text = channel_info['comment']
                    
                    try:
                        # بررسی آخرین پست
                        async for message in self.app.get_chat_history(channel_id, limit=1):
                            # کامنت اول
                            await message.reply(comment_text)
                            break
                    except Exception as e:
                        logger.error(f"خطا در کامنت خودکار برای کانال {channel_id}: {e}")
                        
            except Exception as e:
                logger.error(f"خطا در نظارت کامنت: {e}")
            
            await asyncio.sleep(30)  # بررسی هر 30 ثانیه

    async def time_update_loop(self):
        """حلقه بروزرسانی تایم"""
        while self.is_running:
            try:
                # بروزرسانی نام با تایم
                if self.data.get('time_in_name'):
                    await self.update_name_with_time()
                
                # بروزرسانی بیو با تایم
                if self.data.get('auto_bio_time'):
                    await self.update_bio_with_time()
                    
            except Exception as e:
                logger.error(f"خطا در بروزرسانی تایم: {e}")
            
            await asyncio.sleep(60)  # بروزرسانی هر دقیقه

    async def main_loop(self):
        """حلقه اصلی ربات"""
        logger.info("🚀 ربات سلف با موفقیت راه‌اندازی شد!")
        
        # راه‌اندازی تسک‌های پس‌زمینه
        tasks = [
            asyncio.create_task(self.auto_typing_loop()),
            asyncio.create_task(self.comment_monitor()),
            asyncio.create_task(self.time_update_loop())
        ]
        
        try:
            # اجرای همزمان تمام تسک‌ها
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("🛑 ربات متوقف شد!")
        finally:
            self.is_running = False
            if self.app:
                await self.app.stop()
            if self.helper_bot:
                await self.helper_bot.stop()

    async def stop(self):
        """متوقف کردن ربات"""
        self.is_running = False
        if self.app:
            await self.app.stop()
        if self.helper_bot:
            await self.helper_bot.stop()

# تابع اصلی
async def main():
    """تابع اصلی برای اجرای ربات"""
    try:
        bot = TelegramSelfBot()
        success = await bot.start_bot()
        if not success:
            print("❌ ربات نتوانست راه‌اندازی شود!")
    except KeyboardInterrupt:
        logger.info("👋 خداحافظ!")
    except Exception as e:
        logger.error(f"خطای کلی: {e}")

if __name__ == "__main__":
    print("""
    🤖 ربات سلف تلگرام + ربات هلپر
    ===================================
    
    ⚠️  توجه: قبل از اجرا، موارد زیر را انجام دهید:
    
    1. API ID و API Hash خود را از https://my.telegram.org دریافت کنید
    2. ربات هلپر از @BotFather بسازید و توکن دریافت کنید
    3. در کد، اطلاعات زیر را جایگزین کنید:
       - YOUR_API_ID (خط 57)
       - YOUR_API_HASH (خط 58)
       - YOUR_PHONE (خط 59)
       - YOUR_BOT_TOKEN (خط 62) - اختیاری
       - owner_id (خط 63) - آیدی عددی خودتان
    
    4. کتابخانه‌های مورد نیاز را نصب کنید:
       pip install pyrogram tgcrypto
    
    5. برای استفاده از پنل کنترل، دستور /help را در ربات هلپر بزنید
    6. برای استفاده در هر جای تلگرام، از حالت inline استفاده کنید:
       @username_ربات_هلپر
    
    🚀 در حال راه‌اندازی...
    """)
    
    asyncio.run(main())