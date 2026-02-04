from flask import Flask, render_template, request, jsonify
import requests
import json
from functools import lru_cache
from datetime import datetime
import os 

app = Flask(__name__)

# API Configuration
API_URL = "https://yosintv.github.io/xauusd/2082.json"

# Cache for election data
@lru_cache(maxsize=1)
def get_election_data():
    """Fetch election data from API"""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching election data: {e}")
        return []

def get_candidate_by_id(candidate_id):
    """Get specific candidate by ID"""
    data = get_election_data()
    for candidate in data:
        if candidate.get('CandidateID') == int(candidate_id):
            return candidate
    return None

def get_all_candidates():
    """Get all candidates"""
    return get_election_data()

def get_candidates_by_constituency(state_id, district_name, constituency_id):
    """Get all candidates in a constituency"""
    data = get_election_data()
    return [c for c in data if c.get('STATE_ID') == int(state_id) and 
            c.get('DistrictName') == district_name and 
            c.get('SCConstID') == int(constituency_id)]

def get_statistics():
    """Calculate election statistics"""
    data = get_election_data()
    unique_constituencies = set()
    unique_parties = set()
    total_votes = 0
    
    for candidate in data:
        unique_constituencies.add(f"{candidate.get('STATE_ID')}|{candidate.get('DistrictName')}|{candidate.get('SCConstID')}")
        unique_parties.add(candidate.get('PoliticalPartyName'))
        total_votes += candidate.get('TotalVoteReceived', 0)
    
    return {
        'total_candidates': len(data),
        'total_constituencies': len(unique_constituencies),
        'total_votes': total_votes,
        'total_parties': len(unique_parties),
        'last_updated': datetime.now().isoformat()
    }

def slugify(text):
    """Convert text to URL-friendly slug"""
    return text.lower().replace(' ', '-').replace('/', '-').replace('&', 'and')

# ============= ROUTES =============

@app.route('/')
def index():
    """Main election results page"""
    stats = get_statistics()
    return render_template('index.html', stats=stats)

@app.route('/api/candidates')
def api_candidates():
    """API endpoint for all candidates"""
    data = get_election_data()
    search = request.args.get('search', '').lower()
    state = request.args.get('state', '')
    district = request.args.get('district', '')
    party = request.args.get('party', '')
    
    filtered = data
    
    if search:
        filtered = [c for c in filtered if search in f"{c.get('CandidateName', '')} {c.get('StateName', '')} {c.get('DistrictName', '')} {c.get('PoliticalPartyName', '')}".lower()]
    
    if state:
        filtered = [c for c in filtered if c.get('StateName') == state]
    
    if district:
        filtered = [c for c in filtered if c.get('DistrictName') == district]
    
    if party:
        filtered = [c for c in filtered if c.get('PoliticalPartyName') == party]
    
    return jsonify(filtered)

@app.route('/api/states')
def api_states():
    """Get all states"""
    data = get_election_data()
    states = list(set(c.get('StateName') for c in data if c.get('StateName')))
    return jsonify(sorted(states))

@app.route('/api/districts/<state>')
def api_districts(state):
    """Get districts for a state"""
    data = get_election_data()
    districts = list(set(c.get('DistrictName') for c in data if c.get('StateName') == state))
    return jsonify(sorted(districts))

@app.route('/api/parties')
def api_parties():
    """Get all parties"""
    data = get_election_data()
    parties = list(set(c.get('PoliticalPartyName') for c in data if c.get('PoliticalPartyName')))
    return jsonify(sorted(parties))

@app.route('/api/stats')
def api_stats():
    """Get election statistics"""
    return jsonify(get_statistics())

@app.route('/candidate/<int:candidate_id>')
def candidate_detail(candidate_id):
    """Individual candidate page with SEO"""
    candidate = get_candidate_by_id(candidate_id)
    
    if not candidate:
        return "Candidate not found", 404
    
    # Get constituency candidates for comparison
    constituency_candidates = get_candidates_by_constituency(
        candidate.get('STATE_ID'),
        candidate.get('DistrictName'),
        candidate.get('SCConstID')
    )
    
    # Sort by votes
    constituency_candidates.sort(key=lambda x: x.get('TotalVoteReceived', 0), reverse=True)
    
    # Determine rank
    rank = next((i+1 for i, c in enumerate(constituency_candidates) if c.get('CandidateID') == candidate_id), 0)
    total_in_constituency = len(constituency_candidates)
    
    # Calculate vote percentage
    total_votes_in_constituency = sum(c.get('TotalVoteReceived', 0) for c in constituency_candidates)
    vote_percentage = (candidate.get('TotalVoteReceived', 0) / total_votes_in_constituency * 100) if total_votes_in_constituency > 0 else 0
    
    # Determine if winner
    max_votes = max(c.get('TotalVoteReceived', 0) for c in constituency_candidates) if constituency_candidates else 0
    is_winner = candidate.get('TotalVoteReceived', 0) == max_votes and max_votes > 0
    
    context = {
        'candidate': candidate,
        'rank': rank,
        'total_in_constituency': total_in_constituency,
        'vote_percentage': round(vote_percentage, 2),
        'is_winner': is_winner,
        'constituency_candidates': constituency_candidates[:10],  # Top 10
        'candidate_slug': slugify(candidate.get('CandidateName', '')),
        'party_slug': slugify(candidate.get('PoliticalPartyName', '')),
    }
    
    return render_template('candidate.html', **context)

@app.route('/results')
def results():
    """Election results page"""
    stats = get_statistics()
    return render_template('index.html', stats=stats)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/faq')
def faq():
    """FAQ page"""
    return render_template('faq.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

# ============= HELPER FUNCTIONS =============

@app.template_filter('number_format')
def number_format(value):
    """Format number with thousand separators"""
    try:
        return "{:,}".format(int(value))
    except:
        return value

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run Flask app
    app.run(debug=True, port=5000)
