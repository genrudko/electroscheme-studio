export type VoltageDisplayProfileId =
  | 'gost_r_56303_2014'
  | 'sto_56947007_25_040_70_101_2011'

export type VoltageClassId =
  | '1150'
  | '800'
  | '750'
  | '500'
  | '400'
  | '330'
  | '220'
  | '150'
  | '110'
  | '60'
  | '35'
  | '20'
  | '15'
  | '10'
  | '6'
  | '3'
  | 'below3'

export type VoltageClassColor = {
  id: VoltageClassId
  label: string
  voltageKv: number
  colorName: string
  color: string
  rgb: [number, number, number]
  profileId: VoltageDisplayProfileId
  source: string
}

export const voltageDisplayProfileLabels: Record<VoltageDisplayProfileId, string> = {
  gost_r_56303_2014: 'ГОСТ Р 56303-2014',
  sto_56947007_25_040_70_101_2011: 'СТО ФСК 2011 (позже)',
}

export const gostR56303VoltageClassColors: VoltageClassColor[] = [
  { id: '1150', label: '1150 кВ', voltageKv: 1150, colorName: 'сиреневый', color: 'rgb(205, 138, 255)', rgb: [205, 138, 255], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '800', label: '800 кВ', voltageKv: 800, colorName: 'темно-синий', color: 'rgb(0, 0, 168)', rgb: [0, 0, 168], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '750', label: '750 кВ', voltageKv: 750, colorName: 'темно-синий', color: 'rgb(0, 0, 168)', rgb: [0, 0, 168], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '500', label: '500 кВ', voltageKv: 500, colorName: 'красный', color: 'rgb(213, 0, 0)', rgb: [213, 0, 0], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '400', label: '400 кВ', voltageKv: 400, colorName: 'оранжевый', color: 'rgb(255, 100, 30)', rgb: [255, 100, 30], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '330', label: '330 кВ', voltageKv: 330, colorName: 'зеленый', color: 'rgb(0, 170, 0)', rgb: [0, 170, 0], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '220', label: '220 кВ', voltageKv: 220, colorName: 'желто-зеленый', color: 'rgb(181, 181, 0)', rgb: [181, 181, 0], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '150', label: '150 кВ', voltageKv: 150, colorName: 'хаки', color: 'rgb(170, 150, 0)', rgb: [170, 150, 0], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '110', label: '110 кВ', voltageKv: 110, colorName: 'голубой', color: 'rgb(0, 153, 255)', rgb: [0, 153, 255], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '60', label: '60 кВ', voltageKv: 60, colorName: 'лиловый', color: 'rgb(255, 51, 204)', rgb: [255, 51, 204], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '35', label: '35 кВ', voltageKv: 35, colorName: 'коричневый', color: 'rgb(102, 51, 0)', rgb: [102, 51, 0], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '20', label: '20 кВ', voltageKv: 20, colorName: 'ярко-фиолетовый', color: 'rgb(160, 32, 240)', rgb: [160, 32, 240], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '15', label: '15 кВ', voltageKv: 15, colorName: 'ярко-фиолетовый', color: 'rgb(160, 32, 240)', rgb: [160, 32, 240], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '10', label: '10 кВ', voltageKv: 10, colorName: 'фиолетовый', color: 'rgb(102, 0, 204)', rgb: [102, 0, 204], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '6', label: '6 кВ', voltageKv: 6, colorName: 'темно-зеленый', color: 'rgb(0, 102, 0)', rgb: [0, 102, 0], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: '3', label: '3 кВ', voltageKv: 3, colorName: 'темно-зеленый', color: 'rgb(0, 102, 0)', rgb: [0, 102, 0], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
  { id: 'below3', label: 'ниже 3 кВ', voltageKv: 0.4, colorName: 'серый', color: 'rgb(127, 127, 127)', rgb: [127, 127, 127], profileId: 'gost_r_56303_2014', source: 'ГОСТ Р 56303-2014 / Elektroshema' },
]

export const voltageClassColors = gostR56303VoltageClassColors

export function voltageClassById(id: VoltageClassId | string): VoltageClassColor {
  if (id === '0.4' || id === '1' || id === 'below_3') {
    return gostR56303VoltageClassColors.find((item) => item.id === 'below3')!
  }
  return gostR56303VoltageClassColors.find((item) => item.id === id)
    ?? gostR56303VoltageClassColors.find((item) => item.id === '10')!
}

export function voltageColorById(id: VoltageClassId | string): string {
  return voltageClassById(id).color
}

export function voltageKvById(id: VoltageClassId | string): number {
  return voltageClassById(id).voltageKv
}

export function voltageClassIdFromKv(voltageKv: number): VoltageClassId {
  if (voltageKv >= 1150) return '1150'
  if (voltageKv >= 800) return '800'
  if (voltageKv >= 750) return '750'
  if (voltageKv >= 500) return '500'
  if (voltageKv >= 400) return '400'
  if (voltageKv >= 330) return '330'
  if (voltageKv >= 220) return '220'
  if (voltageKv >= 150) return '150'
  if (voltageKv >= 110) return '110'
  if (voltageKv >= 60) return '60'
  if (voltageKv >= 35) return '35'
  if (voltageKv >= 20) return '20'
  if (voltageKv >= 15) return '15'
  if (voltageKv >= 10) return '10'
  if (voltageKv >= 6) return '6'
  if (voltageKv >= 3) return '3'
  return 'below3'
}

export function voltageColor(voltageKv: number): string {
  return voltageColorById(voltageClassIdFromKv(voltageKv))
}