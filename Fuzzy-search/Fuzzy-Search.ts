import * as sqlite3 from 'sqlite3';
import { findBestMatch } from 'string-similarity';

// Function to retrieve restaurant names from SQLite3 database
function getRestaurantNamesFromDatabase(callback: (names: string[]) => void) {
  const db = new sqlite3.Database('/Users/jpsl/concierge-ai/src/chatmodels/concierge.db');

  db.all('SELECT restaurant_name FROM restaurants', (err: Error | null, rows: { restaurant_name: string }[]) => {
    if (err) {
      console.error(err);
      callback([]);
    } else {
      const names = rows.map(row => row.restaurant_name);
      callback(names);
    }
  });

  db.close();
}

// Function to find the most similar restaurant name
function findMostSimilarRestaurantName(input: string, names: string[]): string | undefined {
  const { bestMatch } = findBestMatch(input, names);
  return bestMatch.target;
}

function Return_Atual_Name(userInput: string, callback: (mostSimilarName: string | undefined) => void) {
  getRestaurantNamesFromDatabase(names => {
    if (names.length > 0) {
      const mostSimilarName = findMostSimilarRestaurantName(userInput, names);

      if (mostSimilarName) {
        console.log(`The most similar restaurant name to "${userInput}" is: ${mostSimilarName}`);
      } else {
        console.log(`No match found for "${userInput}"`);
      }

      callback(mostSimilarName);
    } else {
      console.log('No restaurant names found in the database.');
      callback(undefined);
    }
  });
}

let name: string = "nicoleta";
Return_Atual_Name(name, mostSimilarName => {
  console.log(mostSimilarName);
});
