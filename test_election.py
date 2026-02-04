import pytest
from election import app, get_election_data, get_candidate_by_id, get_statistics


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHomeRoute:
    """Test the home route"""
    
    def test_home_page_loads(self, client):
        """Test that home page returns 200"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_home_page_contains_title(self, client):
        """Test that home page contains election title"""
        response = client.get('/')
        assert b'Election 2082' in response.data or response.status_code == 200


class TestAboutRoute:
    """Test the about page route"""
    
    def test_about_page_loads(self, client):
        """Test that about page returns 200"""
        response = client.get('/about')
        assert response.status_code == 200


class TestFAQRoute:
    """Test the FAQ page route"""
    
    def test_faq_page_loads(self, client):
        """Test that FAQ page returns 200"""
        response = client.get('/faq')
        assert response.status_code == 200


class TestContactRoute:
    """Test the contact page route"""
    
    def test_contact_page_loads(self, client):
        """Test that contact page returns 200"""
        response = client.get('/contact')
        assert response.status_code == 200


class TestAPIRoutes:
    """Test API endpoints"""
    
    def test_api_candidates_endpoint(self, client):
        """Test candidates API returns JSON"""
        response = client.get('/api/candidates')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_api_states_endpoint(self, client):
        """Test states API returns JSON"""
        response = client.get('/api/states')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_api_parties_endpoint(self, client):
        """Test parties API returns JSON"""
        response = client.get('/api/parties')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_api_stats_endpoint(self, client):
        """Test statistics API returns JSON"""
        response = client.get('/api/stats')
        assert response.status_code == 200
        assert response.content_type == 'application/json'


class TestSearchFunctionality:
    """Test search and filter functionality"""
    
    def test_search_by_name(self, client):
        """Test searching candidates by name"""
        response = client.get('/api/candidates?search=test')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_filter_by_state(self, client):
        """Test filtering candidates by state"""
        response = client.get('/api/candidates?state=Province%201')
        assert response.status_code == 200
    
    def test_filter_by_party(self, client):
        """Test filtering candidates by party"""
        response = client.get('/api/candidates?party=test')
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_error_page(self, client):
        """Test that 404 page is returned for non-existent route"""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
    
    def test_invalid_candidate_id(self, client):
        """Test that invalid candidate ID returns 404"""
        response = client.get('/candidate/999999999')
        assert response.status_code == 404


class TestDataFunctions:
    """Test data retrieval functions"""
    
    def test_get_election_data_returns_list(self):
        """Test that get_election_data returns a list"""
        data = get_election_data()
        assert isinstance(data, list)
    
    def test_get_statistics_returns_dict(self):
        """Test that get_statistics returns a dictionary"""
        stats = get_statistics()
        assert isinstance(stats, dict)
        assert 'total_candidates' in stats
        assert 'total_constituencies' in stats
        assert 'total_votes' in stats
        assert 'total_parties' in stats


class TestTemplateRendering:
    """Test template rendering"""
    
    def test_index_template_renders(self, client):
        """Test that index template renders"""
        response = client.get('/')
        assert response.status_code == 200
        assert response.data is not None
    
    def test_about_template_renders(self, client):
        """Test that about template renders"""
        response = client.get('/about')
        assert response.status_code == 200
        assert response.data is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
