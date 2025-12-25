const fs = require('fs');

async function fetchMatches() {
    const today = new Date().toISOString().split('T')[0];
    const url = `https://www.sofascore.com/api/v1/sport/football/scheduled-events/${today}`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        // Transform data to match your API format
        const matches = (data.events || []).map(event => ({
            id: event.id,
            homeTeam: event.homeTeam.name,
            awayTeam: event.awayTeam.name,
            league: event.tournament.name,
            startTime: event.startTimestamp,
            status: event.status.type
        }));

        // Save to a JSON file
        fs.writeFileSync('matches.json', JSON.stringify({
            lastUpdated: new Date().toISOString(),
            date: today,
            matches: matches
        }, null, 2));
        
        console.log(`Successfully updated ${matches.length} matches.`);
    } catch (error) {
        console.error('Error fetching data:', error);
        process.exit(1);
    }
}

fetchMatches();
