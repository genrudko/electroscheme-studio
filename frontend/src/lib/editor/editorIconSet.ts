export type EditorIconId =
  | 'select'
  | 'pan'
  | 'copy'
  | 'paste'
  | 'copyByPoint'
  | 'line'
  | 'rectangle'
  | 'ellipse'
  | 'text'
  | 'connector'
  | 'ruler'
  | 'grid'
  | 'guides'
  | 'layers'
  | 'image'
  | 'export'
  | 'settings'
  | 'collapseRibbon'

export const editorIcons: Record<EditorIconId, string> = {
  select: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3l12 10-6 1.2L8.5 21 5 3z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>',
  pan: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18M3 12h18M12 3l-3 3m3-3 3 3M12 21l-3-3m3 3 3-3M3 12l3-3m-3 3 3 3M21 12l-3-3m3 3-3 3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  copy: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="7" width="11" height="13" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M5 16V5.5A1.5 1.5 0 0 1 6.5 4H15" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
  paste: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 4h6l1 2h3v15H5V6h3l1-2z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M9 10h6M9 14h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  copyByPoint: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="8" width="10" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="6" cy="6" r="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 7.5 12 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  line: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19 19 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
  rectangle: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="6" width="14" height="12" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>',
  ellipse: '<svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="12" rx="7" ry="5" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>',
  text: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 6h14M12 6v13M9 19h6" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
  connector: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 8h5v8h7" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><circle cx="5" cy="8" r="2" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="19" cy="16" r="2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
  ruler: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="7" width="16" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 7v4m4-4v3m4-3v4" stroke="currentColor" stroke-width="1.4"/></svg>',
  grid: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5h14v14H5zM5 10h14M5 15h14M10 5v14M15 5v14" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>',
  guides: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18M3 12h18" stroke="currentColor" stroke-width="1.4" stroke-dasharray="2 3"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg>',
  layers: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4 4 8l8 4 8-4-8-4zm-6 8 6 3 6-3M6 16l6 3 6-3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>',
  image: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="5" width="16" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="m6 17 4-5 3 3 2-2 3 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><circle cx="15.5" cy="9" r="1.4" fill="currentColor"/></svg>',
  export: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v10m0-10 4 4m-4-4-4 4M5 14v5h14v-5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  settings: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M19 13.5v-3l-2.1-.5-.7-1.7 1.1-1.9-2.1-2.1-1.9 1.1-1.7-.7L10.5 2h-3l-.5 2.1-1.7.7-1.9-1.1-2.1 2.1 1.1 1.9-.7 1.7L0 10.5v3l2.1.5.7 1.7-1.1 1.9 2.1 2.1 1.9-1.1 1.7.7.5 2.1h3l.5-2.1 1.7-.7 1.9 1.1 2.1-2.1-1.1-1.9.7-1.7 2.1-.5z" fill="none" stroke="currentColor" stroke-width="1" transform="translate(2 0) scale(.85)"/></svg>',
  collapseRibbon: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 15h14M8 9l4-4 4 4" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}