import type { VoltageDisplayProfileId } from './voltageClasses'

export type DisplayProfileId = 'gost_r_56303_2014' | 'sto_fsk_placeholder'

export type EngineeringSchemaStyleProfile = {
  id: DisplayProfileId
  title: string
  sourceUrl: string
  voltageDisplayProfileId: VoltageDisplayProfileId
  modularGridStepMm: number
  ugoLineWidthMm: number
  electricalConnectionLineWidthMm: number
  busbarUsesVoltageColor: boolean
  busbarConnectionPointFill: string
}

export const engineeringSchemaStyleProfiles: EngineeringSchemaStyleProfile[] = [
  {
    id: 'gost_r_56303_2014',
    title: 'ГОСТ Р 56303-2014',
    sourceUrl: 'https://elektroshema.ru/2009-02-05-22-57-45/ugo-2/144-normalnaya-sxema.html',
    voltageDisplayProfileId: 'gost_r_56303_2014',
    modularGridStepMm: 2.5,
    ugoLineWidthMm: 0.4,
    electricalConnectionLineWidthMm: 0.4,
    busbarUsesVoltageColor: true,
    busbarConnectionPointFill: '#ffffff',
  },
  {
    id: 'sto_fsk_placeholder',
    title: 'СТО ФСК 2011 (позже)',
    sourceUrl: 'https://elektroshema.ru/2009-02-05-22-57-45/ugo-2/144-normalnaya-sxema.html',
    voltageDisplayProfileId: 'gost_r_56303_2014',
    modularGridStepMm: 2.5,
    ugoLineWidthMm: 0.4,
    electricalConnectionLineWidthMm: 0.4,
    busbarUsesVoltageColor: true,
    busbarConnectionPointFill: '#ffffff',
  },
]
