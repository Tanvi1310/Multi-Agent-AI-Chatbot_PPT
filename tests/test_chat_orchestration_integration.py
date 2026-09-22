from fastapi.testclient import TestClient

from app.main import app


def test_chat_endpoint_uses_orchestrator_response():
    client = TestClient(app)

    register = client.post('/api/v1/auth/register', json={
        'email': 'phase3-demo@example.com',
        'username': 'Phase3 Demo',
        'password': 'demo1234',
    })
    assert register.status_code == 200, register.text
    token = register.json()['access_token']

    create = client.post('/api/v1/conversations', json={'title': 'Orchestration chat'}, headers={'Authorization': f'Bearer {token}'})
    assert create.status_code == 200, create.text
    conversation_id = create.json()['id']

    payload = {
        'message': 'Research generative AI trends and create a proposal outline using the uploaded template.',
        'conversation_id': conversation_id,
    }
    response = client.post('/api/v1/chat', json=payload, headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200, response.text
    body = response.json()
    assert 'assistant_reply' in body
    assert body['assistant_reply']
    assert body['citations']
