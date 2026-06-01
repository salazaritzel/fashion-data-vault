'use client'; // We have user interactions on this page, so we need to make it a client component.

// The goal of this file is to fetch the data based on user selection and pass it for display. useState holds your current selection, useEffect triggers a fetch when that selection changes.

import { useState, useEffect } from 'react';
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Field, FieldLabel } from "@/components/ui/field"
import { Trend } from '../lib/definitions';
import TrendBar from '@/app/ui/trendbar';

const FASTAPI_URL = process.env.NEXT_PUBLIC_FASTAPI_URL;

export function DisplayData() {
  const [isLoading, setIsLoading] = useState<boolean>(true); // Manages the loading state of the data fetch.
  const [error, setError] = useState<Error | null>(null);
  const [entityType, setEntityType] = useState<string>('trend'); // Determines which entity type to fetch
  const [timeWindow, setTimeWindow] = useState<number>(30); // Determines the time window for the data fetch
  const [displayResult, setDisplayResult] = useState<Trend[] | null>(null); // Stores the results of the fetch to be displayed on the dashboard

  useEffect(() => {
    let ignore = false; // Ensures your code doesn’t suffer from “race conditions”.
    setError(null); // Resets the error state before each new fetch.
    setIsLoading(true);

    fetchData(entityType, timeWindow).then(result => {
      if (!ignore) {
        setDisplayResult(result);
        setIsLoading(false);
      }
    });

    return () => {
      ignore = true;
    }
  }, [entityType, timeWindow]);
  
  // Receives the et selection and tw selection as arguments and returns the data to be displayed on the dashboard.
  async function fetchData(entityType: string, timeWindow: number): Promise<Trend[]>{
    try {
      const response = await fetch(`${FASTAPI_URL}/api/trends?entity_type=${entityType}&time_window=${timeWindow}`);
      if(!response.ok) {
        throw new Error(`HTTP error, status: ${response.status}`);
      }
      const data = await response.json();
      return data;
    } catch (err) {
      if(err instanceof Error) {
        console.error(`${err.name}: ${err.message}`);
        setError(err);
      } else {
        console.error('Unexpected error:', err);
      }
      return [];
    }
  }

return (
  <>
    {/* Dropdown Menus for Data Display */}
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-2 p-4 mb-4">
      
      {/* Dropdown menu for entity type */}
      <Field className="w-full max-w-48">
        <FieldLabel>Entity Type</FieldLabel>   
        <Select value = {entityType} onValueChange={(value) => {
          setEntityType(value)
          }}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder = "Select entity type"/>
          </SelectTrigger>

          <SelectContent>
            <SelectGroup>
              <SelectItem value="trend">Trends</SelectItem>
              <SelectItem value="brand">Brands</SelectItem>
              <SelectItem value="material">Materials</SelectItem>
              <SelectItem value="season">Seasons</SelectItem>
            </SelectGroup>
          </SelectContent>

        </Select>
      </Field>

      {/* Dropdown menu for time window */}
      <Field className="w-full max-w-48">
        <FieldLabel>Time Window</FieldLabel>
        <Select value = {String(timeWindow)} onValueChange={(value) => {
          setTimeWindow(Number(value))
          }}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder = "Select time window"/>
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectItem value="30">30 days</SelectItem>
              <SelectItem value="60">60 days</SelectItem>
              <SelectItem value="90">90 days</SelectItem>
              <SelectItem value="180">180 days</SelectItem>
              <SelectItem value="365">365 days</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </Field>
    </div>

    {/* Displayed Data Based on Above Selections */}
    <div className = "shadow-md p-4 rounded-lg bg-white ">
      {isLoading && <p>Loading Data...</p>} {/* This is a simple loading state. Replace with a spinner. */}
      {error && <p>{error.message}</p>}
      {!isLoading && !error && <TrendBar data={displayResult ?? []}/>}
    </div>

    {/* Disclaimer for Data Display */}
    <div className="p-2 text-gray-400 italic text-sm">
      Disclaimer: Bar width reflects relative mention frequency within the selected time window, not total coverage.
    </div>
    </>
  );
}