// Central config for the X5 token.
// When you have the real token, fill in CONTRACT_ADDRESS + CHAIN and the
// /api/token route will automatically fetch live data from DexScreener.

export const TOKEN = {
  symbol: 'X5',
  name: 'X5 Token',
  totalSupply: 1_000_000_000,
  // TODO: replace with your real values once the token is deployed.
  contractAddress: '' as string, // e.g. "0xabc...def"
  chain: 'ethereum' as string, // dexscreener chain slug: ethereum | bsc | solana | base ...
  buyUrl: '#', // DEX swap link
}

export const ALLOCATION = [
  {
    key: 'liquidity',
    label: 'Ліквідність',
    value: 50,
    color: '#8cff21',
    desc: 'Заблокована ліквідність у пулі DEX для стабільної торгівлі та захисту від маніпуляцій.',
  },
  {
    key: 'marketing',
    label: 'Маркетинг',
    value: 20,
    color: '#ffd84b',
    desc: 'Просування, партнерства, лістинги та амбасадори спільноти X5.',
  },
  {
    key: 'prize',
    label: 'Prize Pool',
    value: 15,
    color: '#9a5cff',
    desc: 'Призовий фонд для ігрових раундів X5 та винагород активним холдерам.',
  },
  {
    key: 'burn',
    label: 'Спалювання',
    value: 10,
    color: '#ff6244',
    desc: 'Дефляційний механізм: частина токенів періодично вилучається з обігу.',
  },
  {
    key: 'team',
    label: 'Команда',
    value: 5,
    color: '#4d8fff',
    desc: 'Токени команди з вестингом для довгострокової відповідальності проєкту.',
  },
] as const

export type Allocation = (typeof ALLOCATION)[number]
