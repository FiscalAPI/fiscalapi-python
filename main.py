from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.services.fiscalapi_client import FiscalApiClient

def main ():
    print("Hello World!")
    
    settings = FiscalApiSettings(
            api_url="https://test.fiscalapi.com",
            api_key="sk_test_52be6db9_6d23_4191_b39f_cd9cc9df91c2",
            tenant="102e5f13-e114-41dd-bea7-507fce177281",
    )
        
    client = FiscalApiClient(settings=settings)
    
    api_response = client.products.get_by_id("27808326-1824-4f3c-87fb-03ace1066f16")
    
    
    
    print(api_response)
    
    
if __name__ == "__main__":
    main()