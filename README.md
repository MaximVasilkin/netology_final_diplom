# API Сервис заказа товаров для розничных сетей

#### Дипломный проект [по техническому заданию Нетологии](https://github.com/MaximVasilkin/python-final-diplom ) с авторскими модификациями

___

### Настройка

```
git clone https://github.com/MaximVasilkin/netology_final_diplom.git
```

Задать настройки переменных в файле [.env](/.env)

```
docker compose up
```

<br>

**Для работы авторизации через ВК требуется:**

1) перейти на [страницу создания приложения ВК](https://vk.com/editapp?act=create)
2) создать приложение типа ```Сайт```
3) перейти на вкладку ```Настройки```
4) значение поля ```ID приложения``` задать переменной окружения ```SOCIAL_AUTH_VK_OAUTH2_KEY``` в файле [.env](/.env)
5) значение поля ```Защищённый ключ``` задать переменной окружения ```SOCIAL_AUTH_VK_OAUTH2_SECRET``` в файле [.env](/.env)

# Эндпоинты 
<br>

>## [Для покупателя](#buyer)
>## [Для продавца](#seller)


**_Метод, выделенный жирным курсивом_**, - защищённый. \
Для доступа требуется передать в http-запросе заголовок Authorization со значением Token <ваш токен>.\
Например: \
Authorization: Token 124vho6743fsv52f90gd47bxs  

<br>

## <a name="buyer"></a>Для покупателя

### /login/vk-oauth2/

GET - авторизация/регистрация через ВК.\
После запроса выдаётся токен авторизации.
>Новым пользователям системы дополнительно выдается пароль - для авторизации на ресурсе без помощи соц. сети. <br>
Авторизация через ВК недоступна пользователям с неподтверждённой эл. почтой в аккаунте соц. сети.

<br>

### /users/
**_GET_** - получить данные своего текущего пользователя.\

POST - зарегистрировать нового пользователя.\

Пример: 

```

{
    "first_name": "test", 
    "last_name": "test_last_name", 
    "username": "TESTO", 
    "email": "example@mail.ru", 
    "password": "123abc!!!", 
    "password2": "123abc!!!"
}
```

>Для подтверждения регистрации откройте указанную почту и следуйте инструкциям в письме.

**_PATCH_** - изменить данные своего текущего пользователя.

Пример изменения пароля: 

```
{
    "current_password": "123abc!!!", 
    "password": "abcREW222", 
    "password2": "abcREW222"
}
```

>При смене пароля обновляется и токен авторизации.\
Изменить почту (email) нельзя.

<br>

### /users/auth/
POST - авторизация по email и паролю (получить токен авторизации). \
Пользователям с неподтверждённым email-адресом токен не выдаётся.

Пример: 
```
{
    "email": "example@mail.ru", 
    "password": "abcREW222"
}
```

<br>

### /user/password_reset/
POST - отправить на почту запрос с данными, необходимыми для сброса пароля.

Пример:
```
{
    "email": "example@mail.ru"
}
```

<br>

### /user/password_reset/confirm/
POST - сбросить пароль на новый.

Пример:
```
{
    "email": "example@mail.ru", 
    "token": "TOKEN_FROM_EMAIL_MESSAGE", 
    "password": "newpassword123", 
    "password2": "newpassword123"
}
```

>Где token - полученный на предыдущем шаге токен из email-сообщения.\
При сбросе пароля обновляется и токен авторизации.

<br>

### /user/contact/
**_GET_** - получить список всех своих контактов.

**_POST_** - создать контакт.

Пример:
```
{
    "city": "Москва",
    "street": "3-я улица строителей",
    "house": "25",
    "structure": "1",
    "building": "1",
    "apartment": "1",
    "phone": "+79260000000"
}
```

>Количество создаваемых контактов неограниченно.

<br>

### /user/contact/5/
**_GET_** - получить свой контакт с id равным 5.

**_PATCH_** - изменить свой контакт с id равным 5.

Пример:
```
{
    "phone": "+79261234567"
}
```

>Нельзя изменить контакт, который уже использовался в заказе.

**_DELETE_** - удалить свой контакт с id равным 5.

<br>

### /shops/
GET - получить список всех магазинов.

**_POST_** - создать свой магазин.

Пример:
```
{
    "name": "10-ка",
    "url": "http://www.десяточка.рф",
    "email": "10ka@mail.ru"
}
```

>На одну учётную запись пользователя можно создать только 1 магазин.\
После создания магазина учётная запись пользователя автоматически получает статус _Продавец_.

<br>

### /shops/5/
GET - получить магазин с id равным 5.

**_PATCH_** - изменить магазин с id равным 5.
>Изменить можно только свой магазин.

Пример:
```
{
    "name": "Десяточка"
}
```

>Узнать id своего магазина можно при его создании, а также по адресу ```/partner/products/``` или ```/partner/orders/```

<br>

### /categories/
GET - получить список всех категорий товаров, зарегистрированных на ресурсе.

<br>

### /categories/5/
GET - получить категорию с id равным 5.

<br>

### /products/
GET - Получить список всех доступных товаров для заказа.

>Товар не отобразится, если его нет в наличии, или магазин, в котором он продаётся, закрыт.

Доступна фильтрация товаров по:

name = наименование товара ```*```\
shop = название магазина ```*```\
min_price = минимальная цена товара\
max_price = максимальная цена товара\
min_price_rrc = минимальная рекомендованная цена товара для розничной продажи\
max_price_rrc = максимальная рекомендованная цена товара для розничной продажи\
category = категория товара ```*```\
quantity = количество товара в наличии\

>  ```*```  - Данное поле поддерживает неполный ввод и мультизапрос

Примеры:

**Комбинированные фильтры**

Чтобы получить все товары MaxPhone15 по цене от 20000 до 25000, в магазинах MVS и Максилинк,\
нужно отправить GET-запрос на следующий URL:

```
/products/?name=MaxPhone15&min_price=20000&max_price=25000&shop=MVS,Максилинк
```

**Мультизапрос**

Если требуется получить все товары категории Планшеты и Смартфоны:

```
/products/?category=Планшеты,Смартфоны
```

**Неполный ввод**

Чтобы получить весь ассортимент из магазинов MaxStore-аптека, MaxStore-цифровой, MaxStore-косметик:

```
/products/?shop=MaxStore
```

Поля, поддерживающие неполный ввод, включают в поисковую выдачу все результаты, подходящие по искомой ключевой фразе.

>Так, по запросу ```/products/?name=краб``` можно увидеть следующие товары (если они доступны для покупки): \
Крабовые палочки, Блесна в виде краба, Гидрокостюм "краб".

<br>

### /products/5/
GET - получить товар с id равным 5.

<br>

### /basket/
**_GET_** - получить информацию о текущей корзине (если она есть).

**_POST_** - добавить товар(ы)/изменить количество товара(ов) по его(их) id.

Пример:
```
[
    {
        "product_info": 1,
        "quantity": 1
    },
    {
        "product_info": 4,
        "quantity": 5
    }
]
```

>Если переданные в запросе товары уже есть в корзине, то обновляется их заказанное количество значениями из запроса.
Если переданные в запросе товары отсутствуют в корзине, то они просто добавляются в неё.

**_DELETE_** - удалить из корзины товар(ы) с id из списка.

Пример:
```
[4]
```

<br>

### /order/
**_GET_** - получить все свои заказы.

Доступна фильтрация по контактному номеру телефона (phone) и дате размещения заказа (created_at).\
Например, чтобы получить все свои заказы, оформленные до 2023.12.31 на номер +79260000000, \
нужно отправить GET-запрос на следующий URL:

```
/order/?created_at_before=2023-12-31&phone=9260000000
```

**_POST_** - разместить заказ из корзины на предварительно созданный контакт.

Пример:
```
{
    "contact": 1
}
```
Где 1 - id контакта покупателя

>Если заказанное количество товара превышает его фактический остаток, заказ не подтверждается, 
заказанные позиции остаются в корзине, а пользователю возвращается информация о всём его заказе, 
включая информацию о всех товарах, заказанное количество которых превышено.\
В ином случае заказ подтверждается, а покупателю и продавцу(ам) направляется email-уведомление с информацией о новом заказе.

<br>

### /order/5/
**_GET_** - получить свой заказ с id равным 5.

<br>

### /order/seller_order/1/
**_DELETE_** - полностью отменить заказ для магазина, где id заказа магазина равен 1.

Данный запрос отменяет доставку всех заказанных товаров конкретного магазина в ещё не доставленном заказе пользователя.

Как это работает:\
Допустим, заказан планшет, монитор и смартфон.\
При этом, планшет и монитор заказаны из магазина А, а смартфон в магазине Б.\
Сервис группирует заказанные товары из заказа пользователя по мини-подзаказам для магазинов.\
Так, магазин А получит заказ с id (предположим) 1, в составе которого планшет и монитор.\
Магазин Б получит заказ с id (предположим) 2, в составе которого смартфон.\
Пока статус заказа магазина ```Статус корзины```, ```Новый```, ```Подтвержден```, ```Собран``` пользователь может от него отказаться.\
В случае отмены, записанное в базе данных количество товаров на складе 
автоматически увеличивается на количество товаров отменённого заказа, 
магазину направляется email-уведомление об отмене заказа, 
а общая сумма заказа покупателя уменьшается на сумму отменённого заказа продавца.


## <a name="seller"></a>Для продавца

<br>

### /partner/products/upload/
**_POST_** - импорт товаров в формате .yaml.

Требуется к запросу прикрепить файл в [таком формате](/app/data/shop1.yaml).

Все данные проходят валидацию. В случае ошибки будет выдан соответствующий ответ.
Если у пользователя нет магазина, он создастся автоматически, а статус пользователя изменится на "Продавец".
Если ранее магазин был уже создан, а в файле переданы данные другого магазина,
все изменения ассортимента будут применены к уже имеющемуся магазину.\
Если не передан email магазина, он будет взят из профиля пользователя.\
Если не указана базовая цена доставки магазина, она будет равна стандартному значению: 300.\

В случае повторного импорта данные актуализируются следующим образом:\
Если товар с переданным в запросе id отсутствует, он создается.\
Если товар присутствует, но в данных из запроса не было изменено его 
```product_parameters```, ```quantity```, ```price```, ```price_rrc```, товар остаётся без изменений.

В случае, если одно из полей товара ```product_parameters```, ```quantity```, ```price```, ```price_rrc``` (или все) 
были изменены, они полностью обновляются на предоставленные в запросе значения.

>Если в базе данных сервиса есть товары, которые не переданы в запросе (yaml-файле), 
они считаются недоступными для покупки: их количество ```quantity``` становится равным нулю, 
что, в свою очередь, автоматически скрывает их для покупателя из выдачи по адресу ```/products/```

<br>

### /partner/products/
**_GET_** - получить список всех товаров своего магазина.
(отображает все товары, даже если магазин закрыт и/или товара нет в наличии).

Доступна фильтрация товаров по:

name = наименование товара ```*```\
min_price = минимальная цена товара\
max_price = максимальная цена товара\
min_price_rrc = минимальная рекомендованная цена товара для розничной продажи\
max_price_rrc = максимальная рекомендованная цена товара для розничной продажи\
category = категория товара ```*```\
quantity = количество товара в наличии\
product_external_id - фильтрация по внешнему id товара (по id товара из базы данных магазина).\
category_external_id - фильтрация по внешнему id категории (по id категории из базы данных магазина).

> ```*``` - Данное поле поддерживает неполный ввод и мультизапрос

Примеры:

**Комбинированные фильтры**

Чтобы получить все товары MaxPhone15 по цене от 20000 до 25000, количество на складе которых не менее 2 шт., 
нужно отправить GET-запрос на следующий URL:

```
/partner/products/?name=MaxPhone15&quantity=2
```

**Мультизапрос**

Если требуется получить все товары категории Планшеты и Смартфоны:

```
/partner/products/?category=Планшеты,Смартфоны
```

**Неполный ввод**

>Поля, поддерживающие неполный ввод, включают в поисковую выдачу все результаты, подходящие по искомой ключевой фразе.

Так, по следующему запросу:
```
/partner/products/?name=краб
```
Можно увидеть товары:
>Крабовые палочки, Блесна в виде краба, Гидрокостюм "краб".

**_POST_** - создать свой товар.

Пример:
```
{
    "external_id": 100,
    "product": {
        "name": "Арбуз"
    },
    "category": {
            "name": "Продукты",
            "external_id": 15
    },
    "product_parameters": [
        {
            "parameter": "Вес",
            "value": "7 кг"
        },
        {
            "parameter": "Цвет",
            "value": "Жёлтый"
        }
    ],
    "quantity": 50,
    "price": 700,
    "price_rrc": 1000
}
```

>Нельзя создать товар с одинаковым external_id.

<br>

### /partner/products/5/
**_GET_** - получить товар своего магазина с id товара равным 5.

**_PATCH_** - изменить товар своего магазина с id товара равным 5.

Пример:
```
{
    "product_parameters": [
        {
            "parameter": "Вес",
            "value": "7.5 кг"
        },
        {
            "parameter": "Цвет",
            "value": "Жёлтый"
        },
        {
            "parameter": "Форма",
            "value": "Кубический"
        }
    ],
    "price": 900,
    "price_rrc": 1150,
    "quantity": 33
}
```

>Изменить можно только поля товара: ```product_parameters```, ```quantity```, ```price``` и ```price_rrc``` 
(параметры товара, количество в наличии, цену, рекомендованную цену для розничной продажи).\
Если указано поле ```product_parameters```, то соответствующее поле товара полностью заменяется на предоставленные значения.

**_DELETE_** - обнулить количество товара в наличии.

Данное действие также скроет продукт из выдачи по адресу ```/products/```

<br>

### /partner/state/
**_GET_** - получить текущий статус своего магазина.

**_POST_** - изменить статус своего магазина.

>Возможные варианты статуса:\
"on" (Открыто), "off" (Закрыто).

Пример:
```
{
    "state": "off"
}
```

Товары закрытого магазина невидны в поиске товаров по адресу ```/products/```,
и пользователи не могут положить их в корзину.

>Если пользователь успел положить товар в корзину, а продавец сразу "закрыл" магазин, 
то в случае подтверждения заказа пользователем, магазин всё равно получит заказ.\
Принимать ли такой заказ - вопрос рассматривается продавцом в индивидуальном порядке.\
Продавец в праве отказаться от выполнения заказа и может самостоятельно его отменить.

<br>

### /partner/orders/
**_GET_** - получить список всех заказов своего магазина.

Доступна фильтрация по контактному номеру телефона покупателя (phone), 
дате размещения заказа (created_at) и email"у покупателя.

>Например, чтобы получить все заказы магазина, оформленные до 2023.12.31 на номер +79260000000 
и с эл. почтой example@mail.com, нужно отправить GET-запрос на следующий URL:

```
/partner/orders/?created_at_before=2023-12-31&phone=9260000000&email=example@mail.com
```

<br>

### /partner/orders/5/
**_GET_** - получить заказ своего магазина с id равным 5.

**_PATCH_** - изменить заказ своего магазина с id равным 5.

Пример:
```
{
    "state": "delivered"
}
```

>Изменить возможно только поле "state" и "shipping_price" (Статус и Стоимость доставки).

Возможные варианты статуса заказа:

>"new" - Новый\
"confirmed" - Подтверждён\
"assembled" - Собран\
"sent" - Отправлен\
"delivered" - Доставлен\
"canceled" - Отменён

У отменённого (статус "canceled") или доставленного (статус "delivered") заказа обновить статус (state) невозможно.\
Стоимость доставки можно изменить, только если статус заказа ```new```, ```confirmed```, ```assembled``` - (Новый, Подтверждён, Собран).

>В случае установки статуса "canceled" (отменён), записанное в базе данных количество товаров на складе автоматически 
увеличивается на количество товаров отменённого заказа, а общая сумма заказа покупателя уменьшается на сумму заказа, 
отменённого продавцом.\
При любом изменении статуса заказа покупателю направляется email-уведомление.