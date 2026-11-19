# Evidence index — demo-megakino

## Files
| File | Title | Source | Type | Accessed |
|------|-------|--------|------|----------|
| `20261104-info-kinopoisk-join.md` | Инфосообщение: состав МегаКино + Кинопоиск | https://moscow.megafon.ru/help/info/popular/information/20260706-1539.html | page | 2026-11-04 |
| `20261104-megafon-home-megakino.md` | Главная moscow.megafon.ru — упоминание МегаКино | https://moscow.megafon.ru/ | page | 2026-11-04 |
| `20261104-megakino-landing.md` | МегаКино — публичный лендинг услуги | https://moscow.megafon.ru/services/megakino/ | page | 2026-11-04 |
| `20261104-ott-prices-analysis.md` | Table analysis — `ott_price_snapshot.csv` |  |  |  |
| `20261104-press-2023-half-market.md` | Пресс-релиз 2023: расширение МегаКино (исторический контекст) | https://corp.megafon.ru/press/news/federalnye_novosti/federal/20230928-1052.html | page | 2026-11-04 |
| `20261104-review-themes-note.md` | Демо-агрегат тем отзывов (методика) | `inputs/review_themes_aggregate.csv` | table | 2026-11-04 |
| `20261104-reviews-table-analysis.md` | Table analysis — `review_themes_aggregate.csv` |  |  |  |
| `20261104-synthetic-subscriber.md` | SYNTHETIC INTERVIEW — не доказательство спроса |  | synthetic | 2026-11-04 |
| `20261104-ux-landing.md` | UX-разбор публичного лендинга МегаКино | https://moscow.megafon.ru/services/megakino/ | screenshot / page observation | 2026-11-04 |
| `20261119-competitor-ott-angle.md` | Конкурентный угол: одиночная OTT vs операторский пакет | публичные ориентиры цен из `inputs/ott_price_snapshot.csv` + механика МегаКино на https://moscow.megafon.ru/services/megakino/ | other | 2026-11-19 |
| `20261119-new-signal-price-parity.md` | Новый сигнал: паритет цены с одной OTT | `inputs/new_data_20261119_price_hold.md` + `evidence/20261104-info-kinopoisk-join.md` | other | 2026-11-19 |
| `20261119-store-review-themes.md` | Агрегат тем публичных отзывов приложений (метод) | `inputs/store_review_themes_aggregate.csv` (составлено для демо) | review_aggregate | 2026-11-19 |
| `20261119-store-themes-analysis.md` | Table analysis — `store_review_themes_aggregate.csv` |  |  |  |

## Claims
| ID | Type | Text | Source |
|----|------|------|--------|
| C001 | fact | На лендинге МегаКино обещание: «5 кинотеатров по цене одного, а также дополнительные киносервисы». | evidence/20261104-megakino-landing.md |
| C002 | fact | Услуга доступна только абонентам МегаФона. | evidence/20261104-megakino-landing.md |
| C003 | fact | В основные входят START, Wink, КИОН, PREMIER, Кинопоиск — между ними можно переключаться; одновременно активен сценар... | evidence/20261104-megakino-landing.md |
| C004 | fact | Каждые 30 дней доступно 3 бесплатных переключения; далее — 30 ₽ за переключение (или пакеты безлимитных переключений). | evidence/20261104-megakino-landing.md |
| C005 | fact | Дополнительные кинотеатры (Смотрёшка, Wink Дети, Wink Всё в одном, Иви) оплачиваются отдельно и не входят в стоимость... | evidence/20261104-megakino-landing.md |
| C006 | fact | Инфосообщение 06.07.2026: с 16.07.2026 доступны START, Wink, КИОН, PREMIER, Кинопоиск; цена 399 ₽ / 30 дней. | evidence/20261104-info-kinopoisk-join.md |
| C007 | fact | На главной moscow.megafon.ru: «1 доступ — 5 онлайн-кинотеатров и дополнительные киносервисы». | evidence/20261104-megafon-home-megakino.md |
| C008 | fact | Пресс-релиз 28.09.2023 явно формулирует принцип: в моменте пользуются одним кинотеатром, выбор можно изменить. | evidence/20261104-press-2023-half-market.md |
| C009 | fact | Состав сервисов в пресс-релизе 2023 отличается от состава лендинга 2026. | evidence/20261104-press-2023-half-market.md |
| C010 | hypothesis | Hero «пять кинотеатров» без явной механики «один активный» создаёт expectation gap до чтения FAQ. | evidence/20261104-ux-landing.md |
| C011 | hypothesis | Соседство допов с основными на лендинге усиливает ожидание «всё включено». | evidence/20261104-ux-landing.md |
| C012 | hypothesis | Демо-агрегат тем отзывов: доминируют value_unclear_five_vs_one и switching_friction. | evidence/20261104-review-themes-note.md |
| C013 | hypothesis | Синтетический респондент: ценность операторской подписки = один счёт + сезонный выбор одного сервиса, не частый свитч... | evidence/20261104-synthetic-subscriber.md |
| C014 | hypothesis | Синтетический респондент: нужна ясность, как быстро сменить кинотеатр и не потерять прогресс просмотра. | evidence/20261104-synthetic-subscriber.md |
| C015 | fact | Публичный ориентир цены МегаКино: 399 ₽ / 30 дней (инфосообщение + CSV snapshot). | evidence/20261104-info-kinopoisk-join.md |
| C016 | forecast | Если выровнять сообщение hero с механикой «один активный + смена», доля негатива про «обман ожидания» снизится при A/... | outputs/validation_plan.md |
| C017 | fact | На open-data срезе цен одиночные OTT ориентировочно 299–399 ₽ / 30 дней при МегаКино 399 ₽. | evidence/20261119-competitor-ott-angle.md |
| C018 | hypothesis | Демо-агрегат store-тем: value unclear и friction управления услугами — приоритетные барьеры рядом с лендингом. | evidence/20261119-store-review-themes.md |
| C019 | hypothesis | При паритете цены с одним OTT без явной опции смены каталога рациональнее выбрать прямую подписку. | evidence/20261119-new-signal-price-parity.md |
| C020 | fact | На 2026-11-19 публичная цена МегаКино 399 ₽ / 30 дней не изменилась относительно C015. | evidence/20261119-new-signal-price-parity.md |
