# Visio draft symbol review summary

- Draft count: 147
- Loaded count: 147
- With terminals: 109
- Without terminals: 38
- With warnings: 122
- With errors: 0
- Average quality: 95.58

## Categories

| Category | Count |
|---|---:|
| annotation | 9 |
| busbar | 12 |
| circuit_breaker | 7 |
| disconnector | 6 |
| earthing_switch | 21 |
| fuse | 7 |
| kru_trolley | 8 |
| line_grounding | 1 |
| reactor_compensation | 10 |
| stamp_frame | 4 |
| surge_arrester | 8 |
| transformer | 36 |
| unknown | 18 |

## High priority review

| Symbol | Category | Score | Terminals | Errors | Warnings |
|---|---|---:|---:|---:|---:|
| `visio_108_соединение_для_шин` Соединение для шин | busbar | 88 | 0 | 0 | 1 |
| `visio_110_опора_1` Опора 1 | annotation | 88 | 0 | 0 | 1 |
| `visio_111_опора_2` Опора 2 | annotation | 88 | 0 | 0 | 1 |
| `visio_113_автомат_выкл` Автомат (выкл) | transformer | 88 | 0 | 0 | 1 |
| `visio_114_счетчик_прямоточный` Счётчик прямоточный | unknown | 88 | 0 | 0 | 1 |
| `visio_116_master_116` Master 116 | unknown | 88 | 0 | 0 | 1 |
| `visio_117_выключатель_вкл` Выключатель (вкл) | circuit_breaker | 88 | 0 | 0 | 1 |
| `visio_120_выключатель_выкл` Выключатель (выкл) | circuit_breaker | 88 | 0 | 0 | 1 |
| `visio_122_счетчик_птподпись` Счётчик ПТ(Подпись) | unknown | 88 | 0 | 0 | 1 |
| `visio_123_data_graphic39` Data Graphic.39 | unknown | 88 | 0 | 0 | 1 |
| `visio_125_счетчик_тт_подпись` Счётчик ТТ (Подпись) | transformer | 88 | 0 | 0 | 1 |
| `visio_126_data_graphic78` Data Graphic.78 | unknown | 88 | 0 | 0 | 1 |
| `visio_127_счетчик_через_тт` Счётчик (через ТТ) | transformer | 88 | 0 | 0 | 1 |
| `visio_130_счетчик_через_тт2` Счётчик (через ТТ2) | transformer | 88 | 0 | 0 | 1 |
| `visio_131_точка_измерения_2` Точка измерения 2 | unknown | 88 | 0 | 0 | 1 |
| `visio_133_счетчик_через_тт2_2` Счётчик (через ТТ2-2) | transformer | 88 | 0 | 0 | 1 |
| `visio_136_опора_3` Опора 3 | annotation | 88 | 0 | 0 | 1 |
| `visio_137_выключатель_2` Выключатель 2 | circuit_breaker | 88 | 0 | 0 | 1 |
| `visio_143_продажа_ээ_с_линией` Продажа ЭЭ (с линией) | unknown | 88 | 0 | 0 | 1 |
| `visio_144_измерение_зак_стрелка` Измерение (зак.) (стрелка) | annotation | 88 | 0 | 0 | 1 |
| `visio_146_основная_надпись` Основная надпись | stamp_frame | 88 | 0 | 0 | 1 |
| `visio_118_data_graphic102` Data Graphic.102 | unknown | 90 | 0 | 0 | 0 |
| `visio_121_data_graphic105` Data Graphic.105 | unknown | 90 | 0 | 0 | 0 |
| `visio_124_text_callout` Text callout | unknown | 90 | 0 | 0 | 0 |
| `visio_128_зона_ответственности` Зона ответственности | unknown | 90 | 0 | 0 | 0 |
| `visio_129_граница_балансовой_принадлежности` Граница балансовой принадлежности | annotation | 90 | 0 | 0 | 0 |
| `visio_132_стрелочка` Стрелочка | unknown | 90 | 0 | 0 | 0 |
| `visio_134_линия` Линия | line_grounding | 90 | 0 | 0 | 0 |
| `visio_135_граница_2` Граница 2 | annotation | 90 | 0 | 0 | 0 |
| `visio_138_текст_1` Текст 1 | annotation | 90 | 0 | 0 | 0 |
| `visio_139_точка_у_п_п` Точка У/П/П | unknown | 90 | 0 | 0 | 0 |
| `visio_140_граница_текст` Граница текст | annotation | 90 | 0 | 0 | 0 |
| `visio_141_измерение_зак` Измерение (зак.) | unknown | 90 | 0 | 0 | 0 |
| `visio_142_продажа_ээ` Продажа ЭЭ | unknown | 90 | 0 | 0 | 0 |
| `visio_145_измерение_ээ` Измерение ЭЭ | unknown | 90 | 0 | 0 | 0 |
| `visio_147_выделение_прямоугольное` Выделение прямоугольное | stamp_frame | 90 | 0 | 0 | 0 |
| `visio_148_выделение` Выделение  | stamp_frame | 90 | 0 | 0 | 0 |
| `visio_149_текстовый_блок` Текстовый блок | stamp_frame | 90 | 0 | 0 | 0 |
| `visio_32_пересечение` Пересечение | earthing_switch | 96 | 2 | 0 | 2 |
| `visio_38_пересечение_лэп` Пересечение ЛЭП | earthing_switch | 96 | 2 | 0 | 2 |

## Policy

- Drafts stay in `needs_review`.
- Core promotion requires manual review.
- Busbars require parameterization.
- Switching devices require state mapping.
- Rotation/snap/stretch/voltage style must be validated.
