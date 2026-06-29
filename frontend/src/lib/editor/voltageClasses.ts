export type VoltageClassId =
  | '1150'
  | '800'
  | '750'
  | '500'
  | '400'
  | '330'
  | '220'
  | '110'
  | '35'
  | '10'
  | '6'
  | '0.4'

export type VoltageClassColor = {
  id: VoltageClassId
  label: string
  voltageKv: number
  color: string
  rgb: [number, number, number]
  codifierRange: string
}

const LOW_VOLTAGE_COLOR = 'rgb(95, 95, 95)'
const LOW_VOLTAGE_RGB: [number, number, number] = [95, 95, 95]

export const voltageClassColors: VoltageClassColor[] = [
  { id: '1150', label: '1150 кВ', voltageKv: 1150, color: 'rgb(205, 138, 255)', rgb: [205, 138, 255], codifierRange: '1150 кВ' },
  { id: '800', label: '800 кВ', voltageKv: 800, color: 'rgb(0, 0, 168)', rgb: [0, 0, 168], codifierRange: '800/750 кВ' },
  { id: '750', label: '750 кВ', voltageKv: 750, color: 'rgb(0, 0, 168)', rgb: [0, 0, 168], codifierRange: '800/750 кВ' },
  { id: '500', label: '500 кВ', voltageKv: 500, color: 'rgb(213, 0, 0)', rgb: [213, 0, 0], codifierRange: '500 кВ' },
  { id: '400', label: '400 кВ', voltageKv: 400, color: 'rgb(255, 100, 30)', rgb: [255, 100, 30], codifierRange: '400 кВ' },
  { id: '330', label: '330 кВ', voltageKv: 330, color: 'rgb(0, 170, 0)', rgb: [0, 170, 0], codifierRange: '330 кВ' },
  { id: '220', label: '220 кВ', voltageKv: 220, color: 'rgb(255, 210, 0)', rgb: [255, 210, 0], codifierRange: '220 кВ' },
  { id: '110', label: '110 кВ', voltageKv: 110, color: 'rgb(0, 153, 255)', rgb: [0, 153, 255], codifierRange: '110 кВ' },
  { id: '35', label: '35 кВ', voltageKv: 35, color: LOW_VOLTAGE_COLOR, rgb: LOW_VOLTAGE_RGB, codifierRange: '0,4–35 кВ' },
  { id: '10', label: '10 кВ', voltageKv: 10, color: LOW_VOLTAGE_COLOR, rgb: LOW_VOLTAGE_RGB, codifierRange: '0,4–35 кВ' },
  { id: '6', label: '6 кВ', voltageKv: 6, color: LOW_VOLTAGE_COLOR, rgb: LOW_VOLTAGE_RGB, codifierRange: '0,4–35 кВ' },
  { id: '0.4', label: '0,4 кВ', voltageKv: 0.4, color: LOW_VOLTAGE_COLOR, rgb: LOW_VOLTAGE_RGB, codifierRange: '0,4–35 кВ' },
]

export function voltageClassById(id: VoltageClassId | string): VoltageClassColor {
  return voltageClassColors.find((item) => item.id === id) ?? voltageClassColors.find((item) => item.id === '10')!
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
  if (voltageKv >= 110) return '110'
  if (voltageKv >= 35) return '35'
  if (voltageKv >= 10) return '10'
  if (voltageKv >= 6) return '6'
  return '0.4'
}

/**
 * Backward-compatible helper for old code paths that still only know numeric voltage.
 */
export function voltageColor(voltageKv: number): string {
  return voltageColorById(voltageClassIdFromKv(voltageKv))
}