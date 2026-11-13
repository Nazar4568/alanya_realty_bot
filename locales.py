# locales.py

DISTRICTS = [
    "Mahmutlar", "Oba", "Kleopatra", "Kestel",
    "Avsallar", "Kargicak", "Tosmur", "Tepe", "Bektas"
]

TEXTS = {
    "ru": {
        "welcome": "Добро пожаловать! Выберите язык / Оберіть мову / Choose language:",
        "choose_intent": "Чем мы можем вам помочь?",
        "btn_buy": "🏠 Купить недвижимость",
        "btn_sell": "💰 Продать недвижимость",
        "free_text_prompt": (
            "✍️ <b>Вариант 1 (Быстрый с ИИ):</b> Опишите запрос одним сообщением в свободной форме, и ИИ сам заполнит анкету.\n"
            "💡 <i>Пример: «Хочу купить виллу в Махмутларе или Оба, бюджет от 80к до 150к евро»</i>\n\n"
            "👆 <b>Вариант 2 (По шагам):</b> Не хотите печатать текст? Нажмите кнопку ниже — там всего 3 простых вопроса с кнопками (займет 30 секунд)."
        ),
        "btn_manual_mode": "📋 Заполнить по шагам (3 вопроса без ИИ)",
        "analyzing": "⏳ Анализирую ваш запрос...",
        "ask_property_type": "Уточните тип недвижимости:",
        "prop_apartment": "Квартира",
        "prop_house": "Дом",
        "prop_villa": "Вилла",
        "ask_districts": (
            "Выберите один или несколько районов Алании (нажимайте на кнопки, чтобы отметить ✅).\n"
            "Когда закончите, нажмите <b>«Подтвердить»</b>, или нажмите <b>«Не знаю / Любой район»</b>:"
        ),
        "btn_done_districts": "✔️ Подтвердить выбор",
        "btn_skip_districts": "⏭ Не знаю / Любой район",
        "ask_price": (
            "Выберите ваш бюджет в евро кнопкой ниже или напишите свой диапазон вручную.\n"
            "💡 <b>Пример ввода:</b> <code>50000 - 120000</code> или <code>80к-150к</code>"
        ),
        "price_under_70k": "До €70,000",
        "price_70k_120k": "€70,000 – €120,000",
        "price_120k_200k": "€120,000 – €200,000",
        "price_over_200k": "От €200,000+",
        "price_error": "Пожалуйста, выберите вариант на кнопках или введите числа бюджета (например: 70000 - 130000).",
        "summary_card": (
            "📋 <b>Проверьте параметры вашей заявки:</b>\n"
            "• <b>Цель:</b> {intent}\n"
            "• <b>Объект:</b> {prop_type}\n"
            "• <b>Районы:</b> {districts}\n"
            "• <b>Бюджет:</b> {price}"
        ),
        "btn_edit_lead": "🔄 Изменить ответы",
        "ask_contact_prompt": "👇 Оставьте ваш контактный номер телефона (нажмите кнопку ниже или напишите вручную), чтобы риелтор связался с вами:",
        "btn_share_contact": "📱 Поделиться номером телефона",
        "thank_you": "✅ Спасибо! Ваша заявка передана риелтору. Мы свяжемся с вами в ближайшее время."
    },
    "uk": {
        "welcome": "Ласкаво просимо! Оберіть мову:",
        "choose_intent": "Чим ми можемо вам допомогти?",
        "btn_buy": "🏠 Купити нерухомість",
        "btn_sell": "💰 Продати нерухомість",
        "free_text_prompt": (
            "✍️ <b>Варіант 1 (Швидкий з ШІ):</b> Опишіть запит одним повідомленням у вільній формі, і ШІ сам заповнить анкету.\n"
            "💡 <i>Приклад: «Хочу купити віллу в Махмутларі або Оба, бюджет від 80к до 150к євро»</i>\n\n"
            "👆 <b>Варіант 2 (По кроках):</b> Не хочете друкувати текст? Натисніть кнопку нижче — там всього 3 прості питання з кнопками (займе 30 секунд)."
        ),
        "btn_manual_mode": "📋 Заповнити по кроках (3 питання без ШІ)",
        "analyzing": "⏳ Аналізую ваш запит...",
        "ask_property_type": "Уточніть тип нерухомості:",
        "prop_apartment": "Квартира",
        "prop_house": "Будинок",
        "prop_villa": "Вілла",
        "ask_districts": (
            "Оберіть один або декілька районів Аланії (натискайте на кнопки, щоб відмітити ✅).\n"
            "Коли закінчите, натисніть <b>«Підтвердити»</b>, або натисніть <b>«Не знаю / Будь-який район»</b>:"
        ),
        "btn_done_districts": "✔️ Підтвердити вибір",
        "btn_skip_districts": "⏭ Не знаю / Будь-який район",
        "ask_price": (
            "Оберіть ваш бюджет у євро кнопкою нижче або напишіть свій діапазон вручну.\n"
            "💡 <b>Приклад вводу:</b> <code>50000 - 120000</code> або <code>80к-150к</code>"
        ),
        "price_under_70k": "До €70,000",
        "price_70k_120k": "€70,000 – €120,000",
        "price_120k_200k": "€120,000 – €200,000",
        "price_over_200k": "Від €200,000+",
        "price_error": "Будь ласка, оберіть варіант на кнопках або введіть числа бюджету (наприклад: 70000 - 130000).",
        "summary_card": (
            "📋 <b>Перевірте параметри вашої заявки:</b>\n"
            "• <b>Мета:</b> {intent}\n"
            "• <b>Об'єкт:</b> {prop_type}\n"
            "• <b>Райони:</b> {districts}\n"
            "• <b>Бюджет:</b> {price}"
        ),
        "btn_edit_lead": "🔄 Змінити відповіді",
        "ask_contact_prompt": "👇 Залиште ваш контактний номер телефону (натисніть кнопку нижче або напишіть вручну), щоб рієлтор зв'язався з вами:",
        "btn_share_contact": "📱 Поділитися номером телефону",
        "thank_you": "✅ Дякуємо! Ваша заявка передана рієлтору. Ми зв'яжемося з вами найближчим часом."
    },
    "en": {
        "welcome": "Welcome! Choose your language:",
        "choose_intent": "How can we help you today?",
        "btn_buy": "🏠 Buy Property",
        "btn_sell": "💰 Sell Property",
        "free_text_prompt": (
            "✍️ <b>Option 1 (Fast AI mode):</b> Describe what you are looking for in a single message, and AI will fill out the form.\n"
            "💡 <i>Example: «I want to buy a villa in Mahmutlar or Oba, budget 80k to 150k EUR»</i>\n\n"
            "👆 <b>Option 2 (Step-by-step):</b> Prefer not to type? Tap the button below to answer 3 quick multiple-choice questions (takes 30 seconds)."
        ),
        "btn_manual_mode": "📋 Fill out step-by-step (3 quick steps, no AI)",
        "analyzing": "⏳ Analyzing your request...",
        "ask_property_type": "Please specify the property type:",
        "prop_apartment": "Apartment",
        "prop_house": "House",
        "prop_villa": "Villa",
        "ask_districts": (
            "Select one or more districts in Alanya (tap buttons to toggle ✅).\n"
            "When finished, tap <b>«Confirm»</b>, or tap <b>«Not sure / Any district»</b>:"
        ),
        "btn_done_districts": "✔️ Confirm selection",
        "btn_skip_districts": "⏭ Not sure / Any district",
        "ask_price": (
            "Select your budget range in EUR using the buttons below, or type your own range.\n"
            "💡 <b>Example:</b> <code>50000 - 120000</code> or <code>80k-150k</code>"
        ),
        "price_under_70k": "Up to €70,000",
        "price_70k_120k": "€70,000 – €120,000",
        "price_120k_200k": "€120,000 – €200,000",
        "price_over_200k": "€200,000+",
        "price_error": "Please select a button or enter valid budget numbers (e.g., 70000 - 130000).",
        "summary_card": (
            "📋 <b>Please review your request details:</b>\n"
            "• <b>Action:</b> {intent}\n"
            "• <b>Property:</b> {prop_type}\n"
            "• <b>Districts:</b> {districts}\n"
            "• <b>Budget:</b> {price}"
        ),
        "btn_edit_lead": "🔄 Edit answers",
        "ask_contact_prompt": "👇 Please share your contact phone number (tap the button below or type it in) so our realtor can reach out to you:",
        "btn_share_contact": "📱 Share Phone Number",
        "thank_you": "✅ Thank you! Your request has been sent to the realtor. We will contact you shortly."
    }
}