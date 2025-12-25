const fs = require('fs');
const path = require('path');

async function fetchMatches() {
    const today = new Date().toISOString().split('T')[0];
    const url = `https://www.sofascore.com/api/v1/sport/football/scheduled-events/${today}`;
    
    // This ensures the file is saved in the same directory as the script
    const outputPath = path.join(__dirname, 'matches.json');

    try {
        const response = await fetch(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.sofascore.com/'
            }
        });

        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

        const data = await response.json();
        const matches = (data.events || []).map(event => ({
            id: event.id,
            homeTeam: event.homeTeam.name,
            awayTeam: event.awayTeam.name,
            league: event.tournament.name,
            startTime: event.startTimestamp
        }));

        fs.writeFileSync(outputPath, JSON.stringify({
            updatedAt: new Date().toISOString(),
            matches: matches
        }, null, 2));
        
        console.log(`✅ Success! Created matches.json in /data/`);
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

fetchMatches();
