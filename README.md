### Йо-хо-хо, и бутылка рому!
На данный момент каждый мой бот в Telegram хостится на Heroku. Я не знаю почему так получилось, но это было первое
что я нашел в интернете для хостинга скриптов в 2018 году и до сих пор остаюсь пользователем данной платформы.

Тогда было все просто и понятно. В 2018 году ты мог загрузить один скрипт на один аккаунт, который работал 24/7 и это
было абсолютно бесплатно. Можно конечно было загрузить несколько на один аккаунт и это было конечно удобнее, но за это
пришлось бы платить деньги.

И вот где-то в начале 2019 года на Heroku немного поменяли правила. Теперь, на каждый аккаунт дают бесплатно 550 часов работы
любых скриптов бесплатно, потом скрипт уходит в ожидание и ждет либо оплаты дополнительных часов, либо начала следующего
календарного месяца.

Такой расклад, конечно все усугубил. Я сначала подумал что все, надо искать другой хостинг, но нет, я придумал **решение** проблемы.

Я вспомнил, что у Heroku есть API и он оказался достаточно юзабельным. А для Python есть неплохая библиотека для удобства
управления Heroku аккаунтами.

Для каждого аккаунта на Heroku существует отдельный ключ API, который хранится в настройках аккаунта на сайте.
Я решил, что раз уж все равно только одно приложение может уместится на одном аккаунте Heroku, я буду присваивать
в переменную окружения этот API ключ и из него управлять самим аккаунтом.

Но 550 часов в месяц - это где-то 23 дня работы и обычно боты выключались в районе этой даты. Поэтому, я решил создавать
для каждого бота или скрипта по два аккаунта на Heroku. Есть одна проблема конечно, загрузки (deploy) через API с 
github по всей видимости нет. 
> Нет, ну есть конечно автозагрузка прямо внутри аккаунта Heroku, но реализована она через одно место надо отметить.
> Через пару дней авторизация с github аккаунтом слетает и все, автозагрузка перестает работать. Как собственно и обычная,
> нужно заново коннектится к аккаунту github.

Приходится всё же вручную загружать (deploy) своих ботов на оба аккаунта, после каждого их обновления, это единственная проблема.

####Всё остальное берет на себя вот этот скрипт.
Алгоритм весьма прост. Он проверяет сегодняшнюю дату и если наступило 18 число месяца, он сверяет данные в гугл таблице.
> Туда занесены api ключи, остальное я для удобства сверяю: название приложения и почту на которую зареган акк.

В первом столбце - первые аккаунты, в той же строке - вторые. И этот скрипт отключает первые, включает вторые и наоборот 
в первых числах месяца. Этот скрипт не исключение, он тоже продублирован на два аккаунта, просто он перезапускает себя последним.

Вуаля, у нас получается полностью бесплатный хостинг кучи ботов и небольшой костыль, который их обслуживает.

Я почти два года вручную в двадцатых числах перезапускал ботов (ну то есть скрипт был, но запускать его надо было вручную), 
мне было лень допилить его. Только в ноябре 2020 года, я его дописал. Может кому пригодится).

18.11.2020