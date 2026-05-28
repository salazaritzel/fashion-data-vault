// What are we fetching from our database? We want to display the following data on our dashboard:
// 1. Total number of articles saved, relevant? Unsure. 
// 2. What is trending right now so entity type, entity value, and number of mentions. Date?
import 'server-only';
import { Trend } from '../lib/definitions';

const FASTAPI_URL = process.env.FASTAPI_URL;

export async function fetchTrends (): Promise<Trend[]> {
  try {
    const response = await fetch(`${FASTAPI_URL}/api/trends?entity_type=trend&time_window=30`);
    const data = await response.json()
    console.log('Trend data fetch completed.');
    return data;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch trend data.');
  }
}

export async function fetchBrands(): Promise<Trend[]> {
  try {
    const response = await fetch(`${FASTAPI_URL}/api/trends?entity_type=brand&time_window=30`);
    const data = await response.json()
    console.log('Brand data fetch completed.');
    return data;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch brand data.');
  }
}

export async function fetchMaterials(): Promise<Trend[]> {
  try {
    const response = await fetch(`${FASTAPI_URL}/api/trends?entity_type=material&time_window=30`);
    const data = await response.json()
    console.log('Material data fetch completed.');
    return data;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch material data.');
  }
}

export async function fetchSeasons(): Promise<Trend[]> {
  try {
    const response = await fetch(`${FASTAPI_URL}/api/trends?entity_type=season&time_window=30`);
    const data = await response.json()
    console.log('Season data fetch completed.');
    return data;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch season data.');
  }
}