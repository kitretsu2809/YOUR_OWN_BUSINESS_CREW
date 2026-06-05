"""
Contact synchronization with Google Contacts API (People API).
Fetches and caches contacts from Google account.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    from google.auth.oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials as OAuthCredentials
    from google_auth_httplib2 import AuthorizedHttp
    import googleapiclient.discovery
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

# Path to contacts storage
CONTACTS_FILE = Path(__file__).resolve().parents[1] / "contacts.json"

# Google People API scopes
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']


def _load_contacts() -> Dict[str, str]:
    """Load contacts from local JSON file."""
    if CONTACTS_FILE.exists():
        try:
            with open(CONTACTS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def _save_contacts(contacts: Dict[str, str]) -> None:
    """Save contacts to local JSON file."""
    CONTACTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=2)


def _get_credentials():
    """
    Get OAuth2 credentials for Google Contacts API.
    Uses service account or cached OAuth credentials.
    """
    if not GOOGLE_API_AVAILABLE:
        raise ImportError("Google API libraries not installed. Install: pip install google-auth-oauthlib google-api-python-client")
    
    # Try to use service account from environment
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    if service_account_json:
        try:
            return Credentials.from_service_account_file(
                service_account_json,
                scopes=SCOPES
            )
        except Exception as e:
            print(f"Failed to load service account: {e}")
    
    # Fall back to OAuth2 flow (interactive)
    creds = None
    token_path = Path(__file__).resolve().parents[1] / ".google_token.json"
    
    # Load cached token
    if token_path.exists():
        try:
            creds = OAuthCredentials.from_authorized_user_file(token_path, SCOPES)
        except Exception:
            pass
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This requires credentials.json from Google Cloud Console
            credentials_path = Path(__file__).resolve().parents[1] / "credentials.json"
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"credentials.json not found at {credentials_path}\n"
                    "Set up Google OAuth2:\n"
                    "1. Go to https://console.cloud.google.com\n"
                    "2. Create OAuth 2.0 Client ID (Desktop app)\n"
                    "3. Download as credentials.json\n"
                    "4. Place in src/ directory"
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save token for next time
        with open(token_path, 'w') as f:
            f.write(creds.to_json())
    
    return creds


def sync_contacts_from_google() -> Dict[str, int]:
    """
    Fetch contacts from Google Contacts API and save locally.
    
    Returns:
        Dict with 'added', 'updated', 'total' counts
    """
    if not GOOGLE_API_AVAILABLE:
        raise ImportError("Google API libraries not installed")
    
    try:
        credentials = _get_credentials()
    except Exception as e:
        raise RuntimeError(f"Failed to get Google credentials: {e}")
    
    try:
        # Build People API service
        service = googleapiclient.discovery.build('people', 'v1', credentials=credentials)
        
        # Fetch contacts
        results = service.people().connections().list(
            resourceName='people/me',
            personFields='names,emailAddresses',
            pageSize=1000,
            sortOrder='FIRST_NAME_ASCENDING'
        ).execute()
        
        connections = results.get('connections', [])
        
        # Load existing contacts
        local_contacts = _load_contacts()
        added = 0
        updated = 0
        
        # Process fetched contacts
        for person in connections:
            names = person.get('names', [])
            emails = person.get('emailAddresses', [])
            
            if names and emails:
                name = names[0].get('displayName') or \
                       f"{names[0].get('givenName', '')} {names[0].get('familyName', '')}".strip()
                email = emails[0].get('value')
                
                if name and email:
                    if name in local_contacts:
                        if local_contacts[name] != email:
                            local_contacts[name] = email
                            updated += 1
                    else:
                        local_contacts[name] = email
                        added += 1
        
        # Save updated contacts
        _save_contacts(local_contacts)
        
        return {
            'added': added,
            'updated': updated,
            'total': len(local_contacts),
            'message': f"Synced {added} new contacts, updated {updated} existing. Total: {len(local_contacts)}"
        }
    
    except Exception as e:
        raise RuntimeError(f"Failed to sync contacts from Google: {e}")


def get_sync_status() -> Dict:
    """Get current contacts sync status."""
    contacts = _load_contacts()
    return {
        'total_contacts': len(contacts),
        'contacts': contacts
    }
