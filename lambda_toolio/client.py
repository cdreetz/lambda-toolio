import requests
import time
import json
import subprocess
import os
from dotenv import load_dotenv

class LambdaToolio:
    BASE_URL = 'https://cloud.lambdalabs.com/api/v1'

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('LAMBDA_API_KEY')
        if not self.api_key:
            raise ValueError("LAMBDA_API_KEY not found in .env file")
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method, endpoint, data=None, retry_count=3, retry_delay=1):
        url = f"{self.BASE_URL}/{endpoint}"
        for attempt in range(retry_count):
            try:
                response = requests.request(method, url, headers=self.headers, json=data)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == retry_count - 1:
                    raise
                print(f"Request failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

    def check_available_instances(self):
        data = self._make_request('GET', 'instance-types')['data']
        return {
            instance_type: info
            for instance_type, info in data.items()
            if info['regions_with_capacity_available']
        }

    def get_ssh_keys(self):
        return self._make_request('GET', 'ssh-keys')['data']

    def launch_instance(self, instance_type, region, ssh_key_name):
        payload = {
            'region_name': region,
            'instance_type_name': instance_type,
            'ssh_key_names': [ssh_key_name],
            'quantity': 1
        }
        while True:
            try:
                response = self._make_request('POST', 'instance-operations/launch', data=payload)
                return response['data']['instance_ids'][0]
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 400 and "insufficient capacity" in str(e).lower():
                    print("Insufficient capacity. Retrying in 1 second...")
                    time.sleep(1)
                else:
                    raise

    def get_instance_hostname(self, instance_id):
        data = self._make_request('GET', f'instances/{instance_id}')['data']
        return data['hostname']

    def terminate_instances(self):
        instances = self._make_request('GET', 'instances')['data']
        instance_ids = [instance['id'] for instance in instances]
        if instance_ids:
            payload = {'instance_ids': instance_ids}
            return self._make_request('POST', 'instance-operations/terminate', data=payload)
        return None

    def run_ml_script(self, hostname, script_path):
        ssh_command = f'ssh ubuntu@{hostname} "python {script_path}"'
        try:
            subprocess.run(ssh_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running ML script: {e}")

    def interactive_assistant(self):
        print("Welcome to the Lambda Cloud Assistant!")
        
        while True:
            print("\nChecking available instances...")
            available_instances = self.check_available_instances()
            
            if not available_instances:
                print("No instances are currently available. Please try again later.")
                return
            
            print("Available instance types:")
            for i, (instance_type, info) in enumerate(available_instances.items(), 1):
                print(f"{i}. {instance_type} - {info['instance_type']['description']}")
            
            choice = int(input("Enter the number of the instance type you want to launch: ")) - 1
            chosen_instance = list(available_instances.keys())[choice]
            chosen_region = available_instances[chosen_instance]['regions_with_capacity_available'][0]['name']
            
            # Get and display available SSH keys
            ssh_keys = self.get_ssh_keys()
            print("\nAvailable SSH keys:")
            for i, key in enumerate(ssh_keys, 1):
                print(f"{i}. {key['name']}")
            
            key_choice = int(input("Enter the number of the SSH key you want to use: ")) - 1
            ssh_key_name = ssh_keys[key_choice]['name']
            
            print(f"\nAttempting to launch {chosen_instance} in {chosen_region} with SSH key '{ssh_key_name}'...")
            
            try:
                instance_id = self.launch_instance(chosen_instance, chosen_region, ssh_key_name)
                print(f"Instance launched successfully! ID: {instance_id}")
            
                print("\nInstance is getting ready...")
                time.sleep(30)  # Wait for the instance to initialize
                
                hostname = self.get_instance_hostname(instance_id)
                print(f"\nInstance is ready! Hostname: {hostname}")
                
                run_script = input("Do you want to run an ML training script on this instance? (y/n): ").lower()
                if run_script == 'y':
                    script_path = input("Enter the path to your ML script on the remote instance: ")
                    print(f"\nRunning ML script: {script_path}")
                    self.run_ml_script(hostname, script_path)
            except Exception as e:
                print(f"An error occurred: {e}")
            
            terminate = input("Do you want to terminate all running instances? (y/n): ").lower()
            if terminate == 'y':
                result = self.terminate_instances()
                if result:
                    print("All instances have been terminated.")
                else:
                    print("No instances to terminate.")
            
            another = input("Do you want to launch another instance? (y/n): ").lower()
            if another != 'y':
                print("Thank you for using the Lambda Cloud Assistant!")
                break

def main():
    client = LambdaCloudClient()
    client.interactive_assistant()

if __name__ == "__main__":
    main()