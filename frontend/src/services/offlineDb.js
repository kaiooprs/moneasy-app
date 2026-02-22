import Dexie from 'dexie';

export const db = new Dexie('MoneasyOffline');

db.version(1).stores({
  transactions: '++id, amount, description, date, category, synced'
});