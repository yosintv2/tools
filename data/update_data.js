const fs = require('fs');
const path = require('path');

const API_URL = 'https://www.onlinekhabar.com/wp-json/okapi/v2/recent-news';
const DATA_PATH = path.join(__dirname, 'recent.json');

async function updateData() {
    try {
        console.log('Starting update script...');

        // 1. Load existing data safely
        let existingData = [];
        if (fs.existsSync(DATA_PATH)) {
            try {
                const raw = fs.readFileSync(DATA_PATH, 'utf8');
                existingData = JSON.parse(raw || '[]');
                console.log(`Loaded ${existingData.length} existing items.`);
            } catch (e) {
                console.log('recent.json was empty or invalid, starting fresh.');
                existingData = [];
            }
        }

        // 2. Fetch new data
        console.log(`Fetching from: ${API_URL}`);
        const response = await fetch(API_URL);
        
        if (!response.ok) {
            throw new Error(`API returned status ${response.status}`);
        }

        const newData = await response.json();
        console.log(`Fetched ${newData.length} items from API.`);

        // 3. Merge without duplicates (using 'id' as the key)
        const existingIds = new Set(existingData.map(item => item.id));
        const filteredNewItems = newData.filter(item => !existingIds.has(item.id));

        // Prepend new items to the top
        const finalData = [...filteredNewItems, ...existingData];

        // 4. Save file
        fs.writeFileSync(DATA_PATH, JSON.stringify(finalData, null, 2));
        console.log(`Done! Added ${filteredNewItems.length} new items. Total: ${finalData.length}`);

    } catch (error) {
        console.error('CRITICAL ERROR:', error.message);
        process.exit(1); // Tells GitHub Action that something failed
    }
}

updateData();
