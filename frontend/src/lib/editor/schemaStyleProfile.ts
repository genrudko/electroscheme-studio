import type { VoltageDisplayProfileId } from './voltageClasses'

export type DisplayProfileId =
  | 'gost_r_56303_2014'
  | 'sto_fsk_placeholder'

export type EngineeringSchemaStyleProfile = {
  id: DisplayProfileId
  title: string
  sourceTitle: string
  sourceUrl: string
  voltageDisplayProfileId: VoltageDisplayProfileId
  modularGridStepMm: number
  ugoLineWidthMm: number
  electricalConnectionLineWidthMm: number
  busbarUsesVoltageColor: boolean
  busbarConnectionPointFill: string
  busbarConnectionPointStroke: string
  note: string
}

export const engineeringSchemaStyleProfiles: EngineeringSchemaStyleProfile[] = [
  {
    id: 'gost_r_56303_2014',
    title: 'ГОСТ Р 56303-2014',
    sourceTitle: 'Нормальные схемы электрических соединений объектов электроэнергетики',
    sourceUrl: 'https://elektroshema.ru/2009-02-05-22-57-45/ugo-2/144-normalnaya-sxema.html',
    voltageDisplayProfileId: 'gost_r_56303_2014',
    modularGridStepMm: 2.5,
    ugoLineWidthMm: 0.4,
    electricalConnectionLineWidthMm: 0.4,
    busbarUsesVoltageColor: true,
    busbarConnectionPointFill: '#ffffff',
    busbarConnectionPointStroke: '#111827',
    note: 'Базовый профиль редактора. Цвета напряжений, шаг сетки и толщины линий взяты из источника по ГОСТ Р 56303-2014.',
  },
  {
    id: 'sto_fsk_placeholder',
    title: 'СТО ФСК 2011 (позже)',
    sourceTitle: 'СТО 56947007-25.040.70.101-2011',
    sourceUrl: 'https://elektroshema.ru/2009-02-05-22-57-45/ugo-2/144-normalnaya-sxema.html',
    voltageDisplayProfileId: 'gost_r_56303_2014',
    modularGridStepMm: 2.5,
    ugoLineWidthMm: 0.4,
    electricalConnectionLineWidthMm: 0.4,
    busbarUsesVoltageColor: true,
    busbarConnectionPointFill: '#ffffff',
    busbarConnectionPointStroke: '#111827',
    note: 'Зарезервировано. Полный профиль СТО ФСК будет добавлен отдельно, чтобы не смешивать правила.',
  },
]

export const defaultEngineeringSchemaStyleProfile = engineeringSchemaStyleProfiles[0]

export function schemaStyleProfileById(id: DisplayProfileId | string): EngineeringSchemaStyleProfile {
  return engineeringSchemaStyleProfiles.find((profile) => profile.id === id) ?? defaultEngineeringSchemaStyleProfile
}