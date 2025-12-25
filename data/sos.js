const fs = require('fs');
const path = require('path');

async function fetchMatches() {
    const today = new Date().toISOString().split('T')[0];
    // Using the mobile API endpoint sometimes helps bypass desktop blocks
    const url = `https://api.sofascore.com/api/v1/sport/football/scheduled-events/${today}`;
    
    const outputPath = path.join(__dirname, 'matches.json');

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'authority': 'api.sofascore.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'origin': 'https://www.sofascore.com',
                'referer': 'https://www.sofascore.com/',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        });

        if (response.status === 403) {
            throw new Error("403 Forbidden: GitHub IP is being blocked. Try changing the API endpoint.");
        }

        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

        const data = await response.json();
        
        // Match the filtering logic from your original YoSinTV tool
        const matches = (data.events || []).map(event => ({
            id: event.id,
            homeTeam: event.homeTeam.name,
            awayTeam: event.awayTeam.name,
            league: event.tournament.name,
            slug: (event.homeTeam.name + " " + event.awayTeam.name).toLowerCase().replace(/[^a-z0-9]/g, ''),
            timestamp: event.startTimestamp,
            status: event.status.type
        }));

        fs.writeFileSync(outputPath, JSON.stringify({
            updatedAt: new Date().toISOString(),
            date: today,
            matches: matches
        }, null, 2));
        
        console.log(`✅ Success! ${matches.length} matches saved.`);
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

fetchMatches();
