const fs = require('fs');

async function fetchMatches() {
    const today = new Date().toISOString().split('T')[0];
    const url = `https://www.sofascore.com/api/v1/sport/football/scheduled-events/${today}`;
    
    console.log(`Fetching matches for: ${today}`);

    try {
        const response = await fetch(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Referer': 'https://www.sofascore.com/'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (!data.events) {
            throw new Error('No events found in API response');
        }

        const matches = data.events.map(event => ({
            id: event.id,
            homeTeam: event.homeTeam.name,
            awayTeam: event.awayTeam.name,
            league: event.tournament.name,
            category: event.tournament.category.name,
            startTime: event.startTimestamp,
            status: event.status.description
        }));

        fs.writeFileSync('matches.json', JSON.stringify({
            lastUpdated: new Date().toISOString(),
            totalMatches: matches.length,
            matches: matches
        }, null, 2));
        
        console.log(`✅ Success! Saved ${matches.length} matches to matches.json`);
    } catch (error) {
        console.error('❌ Script Failed:', error.message);
        process.exit(1); // This triggers the Exit Code 1 you saw
    }
}

fetchMatches();
