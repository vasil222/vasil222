// Central config for the X5 token.
// When you have the real token, fill in CONTRACT_ADDRESS + CHAIN and the
// /api/token route will automatically fetch live data from DexScreener.

export const TOKEN = {
  symbol: 'X5',
  name: 'X5 Token',
  totalSupply: 1_000_000_000,
  // TODO: replace with your real values once the token is deployed.
  contractAddress: '' as string, // Solana mint address, e.g. "So1111...1112"
  chain: 'solana' as string, // dexscreener chain slug: solana | ethereum | bsc | base ...
  // Solana RPC endpoint used for wallet connection / balances.
  rpcEndpoint: 'https://api.mainnet-beta.solana.com',
  // DEX swap link (e.g. Jupiter/Raydium). Falls back to Jupiter with the mint when set.
  buyUrl: '' as string,
}

// Build a Jupiter swap link when a mint is configured, otherwise return null.
export function getBuyUrl(): string | null {
  if (TOKEN.buyUrl) return TOKEN.buyUrl
  if (TOKEN.contractAddress) {
    return `https://jup.ag/swap/SOL-${TOKEN.contractAddress}`
  }
  return null
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
