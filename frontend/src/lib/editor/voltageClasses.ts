export type VoltageClassColor = {
  id: string
  label: string
  voltageKv: number
  color: string
  rgb: [number, number, number]
}

export const voltageClassColors: VoltageClassColor[] = [
  { id: '1150', label: '1150 кВ', voltageKv: 1150, color: 'rgb(205, 138, 255)', rgb: [205, 138, 255] },
  { id: '800', label: '800 кВ / 750 кВ', voltageKv: 800, color: 'rgb(0, 0, 168)', rgb: [0, 0, 168] },
  { id: '750', label: '750 кВ', voltageKv: 750, color: 'rgb(0, 0, 168)', rgb: [0, 0, 168] },
  { id: '500', label: '500 кВ', voltageKv: 500, color: 'rgb(213, 0, 0)', rgb: [213, 0, 0] },
  { id: '400', label: '400 кВ', voltageKv: 400, color: 'rgb(255, 100, 30)', rgb: [255, 100, 30] },
  { id: '330', label: '330 кВ', voltageKv: 330, color: 'rgb(0, 170, 0)', rgb: [0, 170, 0] },
  { id: '220', label: '220 кВ', voltageKv: 220, color: 'rgb(255, 210, 0)', rgb: [255, 210, 0] },
  { id: '110', label: '110 кВ', voltageKv: 110, color: 'rgb(0, 153, 255)', rgb: [0, 153, 255] },
  { id: '35', label: '0,4–35 кВ', voltageKv: 35, color: 'rgb(95, 95, 95)', rgb: [95, 95, 95] },
  { id: '10', label: '10 кВ', voltageKv: 10, color: 'rgb(95, 95, 95)', rgb: [95, 95, 95] },
  { id: '6', label: '6 кВ', voltageKv: 6, color: 'rgb(95, 95, 95)', rgb: [95, 95, 95] },
  { id: '0.4', label: '0,4 кВ', voltageKv: 0.4, color: 'rgb(95, 95, 95)', rgb: [95, 95, 95] },
]

export function voltageColor(voltageKv: number): string {
  if (voltageKv >= 1150) return 'rgb(205, 138, 255)'
  if (voltageKv >= 750) return 'rgb(0, 0, 168)'
  if (voltageKv >= 500) return 'rgb(213, 0, 0)'
  if (voltageKv >= 400) return 'rgb(255, 100, 30)'
  if (voltageKv >= 330) return 'rgb(0, 170, 0)'
  if (voltageKv >= 220) return 'rgb(255, 210, 0)'
  if (voltageKv >= 110) return 'rgb(0, 153, 255)'
  return 'rgb(95, 95, 95)'
}