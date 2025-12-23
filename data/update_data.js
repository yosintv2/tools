const fs = require('fs');
const path = require('path');

const API_URL = 'https://www.onlinekhabar.com/wp-json/okapi/v2/recent-news';
// Points to recent.json in the same folder as this script
const DATA_PATH = path.join(__dirname, 'recent.json');

async function updateData() {
    try {
        let existingData = [];
        if (fs.existsSync(DATA_PATH)) {
            const raw = fs.readFileSync(DATA_PATH, 'utf8');
            existingData = JSON.parse(raw || '[]');
        }

        const response = await fetch(API_URL);
        const newData = await response.json();

        const existingIds = new Set(existingData.map(item => item.id));
        const filteredNewData = newData.filter(item => !existingIds.has(item.id));

        // New data on top, old data remains below
        const finalData = [...filteredNewData, ...existingData];

        fs.writeFileSync(DATA_PATH, JSON.stringify(finalData, null, 2));
        console.log(`Successfully added ${filteredNewData.length} new items.`);
    } catch (error) {
        console.error('Update failed:', error);
        process.exit(1);
    }
}

updateData();
