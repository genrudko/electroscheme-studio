# Visio Interoperability Contract — ElectroScheme Studio

Статус: canonical architecture/product contract  
Work item: `PROJECT-REFOUNDATION-001`

## 1. Решение

Совместимость с Microsoft Visio является обязательным условием практического внедрения ElectroScheme Studio на российском рынке энергетических схем.

Она нужна не как дополнительный импортёр, а как переходный мост для организаций, у которых:

- действующие схемы хранятся в Visio;
- собственные библиотеки выполнены в VSSX/VSS;
- обмен с подрядчиками и подразделениями выполняется через VSDX/VSD;
- часть пользователей продолжит открывать результат в Visio в переходный период.

Продукт, требующий вручную перерисовать накопленный архив, не считается закрывающим целевую нишу.

## 2. Граница совместимости

Внутренняя модель ElectroScheme Studio не является VSDX-моделью и не должна подчиняться ограничениям Visio.

```text
VSDX/VSSX/VSD/VSS
→ import/interoperability adapter
→ diagnostics and normalization
→ canonical ProjectDocument
→ editing and engineering semantics
→ VSDX export adapter
```

Visio используется как внешний формат миграции и обмена. Каноническим форматом проекта остаётся собственный открытый версионируемый формат ElectroScheme Studio.

## 3. Обязательные направления

### 3.1 Вход в ElectroScheme Studio

Обязательны:

- открытие документов `.vsdx`;
- импорт библиотек `.vssx`;
- чтение masters, instances, groups, pages, layers и relationships;
- чтение размеров страницы, ориентации и масштаба;
- чтение геометрии и трансформаций;
- чтение текста и основных параметров форматирования;
- чтение connection points и connectors;
- чтение Shape Data/custom properties;
- сохранение source IDs, formulas и provenance;
- сопоставление известных masters с принятыми SymbolDefinition;
- отчёт о каждом неподдержанном или неоднозначном элементе.

### 3.2 Выход из ElectroScheme Studio

Обязателен экспорт поддерживаемого электротехнического подмножества в `.vsdx`, чтобы файл:

- открывался в поддерживаемой версии Microsoft Visio;
- сохранял листы, размеры, основную графику, текст и соединители;
- сохранял редактируемость поддерживаемых объектов, а не превращал всю схему в одну картинку;
- содержал Shape Data там, где существует определённое mapping-правило;
- сопровождался отчётом об экспортных ограничениях;
- не выдавался за lossless round-trip, если ограничения присутствуют.

PDF/SVG не заменяют VSDX-экспорт, поскольку не обеспечивают переходное редактирование в Visio.

## 4. Уровни совместимости

### Level A — source inspection

- открыть пакет;
- получить структуру и diagnostics;
- ничего не потерять молча;
- не считать импорт успешным только потому, что XML разобран.

### Level B — VSSX library migration

- извлечь masters;
- сохранить ShapeSheet source data;
- построить review candidates;
- сопоставить с инженерными families;
- не продвигать автоматически в принятую библиотеку.

### Level C — editable VSDX import

- импортировать поддерживаемые объекты в canonical model;
- восстановить листы, компоновку и связи в пределах compatibility profile;
- выделить unsupported/opaque content;
- выдать подробный import report.

### Level D — editable VSDX export

- сформировать корректный `.vsdx` из поддерживаемого ProjectDocument;
- открыть результат в Visio;
- сохранить редактируемые shapes/connectors/text;
- выдать export report.

### Level E — controlled round-trip

Для утверждённого compatibility corpus:

```text
VSDX
→ import
→ no-op export
→ open in Visio
→ compare
```

Должны сохраняться утверждённые категории данных в пределах заданных tolerances.

### Не обещается

Не является целью ранних версий:

- полная бинарная идентичность любого произвольного Visio-файла;
- выполнение произвольных VBA-макросов;
- стопроцентное воспроизведение всех ShapeSheet-функций, add-ons и ActiveX/OLE;
- безусловный round-trip неизвестных сторонних masters;
- поддержка каждого офисного типа диаграмм Visio;
- сохранение внутренних служебных деталей пакета, не влияющих на принятый результат.

## 5. Поддерживаемое электротехническое подмножество

Первый compatibility profile должен быть ориентирован на реальные энергетические схемы и включать как минимум:

- многостраничные VSDX-документы;
- страницы стандартных и пользовательских размеров;
- обычные shapes и groups;
- masters и instances;
- MoveTo/LineTo и необходимые для corpus кривые/дуги;
- position, size, rotation, flip и group transforms;
- текстовые блоки и базовое форматирование;
- линии, штрихи, окончания, fill и visibility;
- динамические/обычные connectors;
- connection points;
- слои и их видимость;
- Shape Data/custom properties;
- изображения и подложки как контролируемый foreign/visual content;
- hyperlinks/cross-page references — после отдельного mapping decision.

Точный профиль формируется по реальному пользовательскому corpus, а не по абстрактному желанию поддержать весь стандарт.

## 6. Неподдерживаемые элементы

Запрещено:

- молча удалять неподдерживаемые shapes;
- заменять сложную геометрию прямоугольником без blocking diagnostic;
- превращать connector в несвязанную линию без явного отчёта;
- считать визуальное совпадение доказательством сохранения topology/Shape Data;
- перезаписывать исходный Visio-файл при импорте;
- скрывать потерю формул, слоёв, текста, групп или properties.

Допустимые стратегии:

- `mapped` — полностью сопоставлено с canonical model;
- `preserved_foreign` — сохранено как opaque foreign object с provenance;
- `visual_fallback` — сохранено как заблокированная визуальная подложка при явном предупреждении;
- `unsupported_blocking` — импорт/экспорт остановлен для критичного элемента;
- `unsupported_nonblocking` — операция разрешена только после просмотра отчёта пользователем.

Исходный файл и его hash должны сохраняться в migration evidence до подтверждения результата.

## 7. Электротехническая семантика

Импортированная фигура Visio не становится автоматически электротехническим объектом.

Mapping должен отдельно установить:

- equipment family;
- equipment identity policy;
- port roles;
- phase/connection semantics;
- allowed states;
- property mapping;
- normative presentation mapping;
- confidence/review state.

Неизвестная фигура может быть сохранена графически, но не должна участвовать в topology/validation как принятый аппарат без инженерной классификации.

## 8. Legacy VSD/VSS

Бинарные форматы `.vsd` и `.vss` должны быть включены в исследование пользовательского corpus.

Начальная стратегия:

- нативная поддержка `.vsdx/.vssx` обязательна;
- для `.vsd/.vss` должен существовать документированный migration path;
- решение о собственном binary parser, локальном conversion adapter или Windows-only bridge принимается после evidence spike;
- наличие старых файлов не должно обнаружиться только на Pilot.

Поддержка `.vsd/.vss` не может незаметно требовать облачного конвертера или передачи рабочих схем внешнему сервису.

## 9. Архитектурные требования

Interoperability subsystem должен быть отделён от:

- canonical document core;
- interactive renderer;
- accepted symbol registry;
- normative profiles;
- topology services.

Обязательные сущности:

- `VisioSourcePackage`;
- `VisioImportProfileVersion`;
- `VisioExportProfileVersion`;
- `ImportDiagnostic`;
- `ExportDiagnostic`;
- `ForeignObjectPayload`;
- `SourceObjectReference`;
- `MappingRuleVersion`;
- `CompatibilityReport`.

Любой imported object должен иметь трассировку к source page/master/shape ID, если источник это позволяет.

## 10. Тестовый corpus

До объявления совместимости требуется corpus из:

- реальных нормальных/главных/однолинейных схем пользователя с обезличиванием при необходимости;
- реальных VSSX/VSS-библиотек;
- grouped shapes;
- сложных masters;
- connectors и connection points;
- custom properties;
- многостраничных документов;
- различных размеров страниц;
- файлов, созданных разными версиями Visio;
- synthetic fixtures для известных edge cases;
- файлов с заведомо неподдерживаемым содержимым.

Corpus должен хранить ожидаемые результаты и лицензионно допустимые test fixtures. Чувствительные реальные схемы не публикуются в открытых artifacts.

## 11. Acceptance gates

### Architecture spike gate

Следующий desktop/platform/core spike обязан доказать:

- чтение контролируемого VSDX fixture;
- запись минимального корректного VSDX fixture;
- открытие экспортированного файла в Visio на Windows;
- работу Python/helper integration без обязательного network access;
- переносимость выбранной архитектуры на Linux, даже если проверка самим Visio выполняется на Windows.

### MVP gate

Core editor MVP может быть принят на собственном формате, но не считается готовым к Pilot/рынку без:

- editable import утверждённого VSDX subset;
- VSSX library migration path;
- compatibility report;
- сохранения source provenance;
- отсутствия silent data loss.

### Pilot gate

До Pilot обязательны:

- экспорт поддерживаемой схемы в VSDX;
- открытие и базовое редактирование результата в Visio;
- controlled round-trip corpus;
- перечень известных ограничений;
- документированный путь для legacy VSD/VSS corpus;
- владелец подтверждает, что реальную рабочую схему не требуется перерисовывать с нуля.

## 12. Продуктовый критерий успеха

Visio interoperability считается успешной, когда пользователь может:

1. взять существующую рабочую схему или библиотеку;
2. импортировать её без скрытых потерь;
3. увидеть точный отчёт о том, что распознано и что требует проверки;
4. продолжить редактирование в ElectroScheme Studio;
5. сохранить инженерную семантику в собственном формате;
6. при необходимости передать поддерживаемую редакцию обратно пользователю Visio.

Совместимость — это управляемая миграция и обмен, а не декларация «мы читаем XML внутри VSDX».
