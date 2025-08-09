#!/usr/bin/env python3
"""
AWS Architecture Diagram Generator for Modern Voting App
Creates a visual representation of the AWS deployment architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_aws_architecture_diagram():
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Define colors
    colors = {
        'aws_orange': '#FF9900',
        'aws_blue': '#232F3E',
        'vpc_blue': '#4A90E2',
        'public_green': '#7ED321',
        'private_orange': '#F5A623',
        'database_purple': '#9013FE',
        'cache_red': '#D0021B',
        'container_teal': '#50E3C2',
        'load_balancer': '#BD10E0',
        'monitoring': '#B8E986'
    }
    
    # Title
    ax.text(8, 11.5, 'Modern Voting App - AWS Architecture', 
            fontsize=20, fontweight='bold', ha='center', color=colors['aws_blue'])
    
    # AWS Cloud boundary
    aws_cloud = FancyBboxPatch((0.5, 0.5), 15, 10.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#F0F8FF', 
                               edgecolor=colors['aws_orange'], 
                               linewidth=3)
    ax.add_patch(aws_cloud)
    ax.text(1, 10.8, 'AWS Cloud', fontsize=14, fontweight='bold', color=colors['aws_orange'])
    
    # VPC
    vpc = FancyBboxPatch((1, 1), 14, 9.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor='#E8F4FD', 
                         edgecolor=colors['vpc_blue'], 
                         linewidth=2)
    ax.add_patch(vpc)
    ax.text(1.5, 10.2, 'VPC (10.0.0.0/16)', fontsize=12, fontweight='bold', color=colors['vpc_blue'])
    
    # Availability Zones
    az1 = FancyBboxPatch((1.5, 1.5), 6, 8.5, 
                         boxstyle="round,pad=0.05", 
                         facecolor='#F9F9F9', 
                         edgecolor='gray', 
                         linewidth=1, linestyle='--')
    ax.add_patch(az1)
    ax.text(1.8, 9.7, 'Availability Zone A', fontsize=10, color='gray')
    
    az2 = FancyBboxPatch((8.5, 1.5), 6, 8.5, 
                         boxstyle="round,pad=0.05", 
                         facecolor='#F9F9F9', 
                         edgecolor='gray', 
                         linewidth=1, linestyle='--')
    ax.add_patch(az2)
    ax.text(8.8, 9.7, 'Availability Zone B', fontsize=10, color='gray')
    
    # Internet Gateway
    igw = FancyBboxPatch((7, 10.5), 2, 0.8, 
                         boxstyle="round,pad=0.05", 
                         facecolor=colors['aws_orange'], 
                         edgecolor='black')
    ax.add_patch(igw)
    ax.text(8, 10.9, 'Internet\nGateway', fontsize=9, ha='center', va='center', color='white', fontweight='bold')
    
    # Application Load Balancer
    alb = FancyBboxPatch((6.5, 8.5), 3, 0.8, 
                         boxstyle="round,pad=0.05", 
                         facecolor=colors['load_balancer'], 
                         edgecolor='black')
    ax.add_patch(alb)
    ax.text(8, 8.9, 'Application Load Balancer', fontsize=9, ha='center', va='center', color='white', fontweight='bold')
    
    # Public Subnets
    pub_subnet1 = FancyBboxPatch((2, 7.5), 5, 1.5, 
                                 boxstyle="round,pad=0.05", 
                                 facecolor=colors['public_green'], 
                                 edgecolor='black', alpha=0.3)
    ax.add_patch(pub_subnet1)
    ax.text(2.2, 8.7, 'Public Subnet A\n10.0.1.0/24', fontsize=9, color='black', fontweight='bold')
    
    pub_subnet2 = FancyBboxPatch((9, 7.5), 5, 1.5, 
                                 boxstyle="round,pad=0.05", 
                                 facecolor=colors['public_green'], 
                                 edgecolor='black', alpha=0.3)
    ax.add_patch(pub_subnet2)
    ax.text(9.2, 8.7, 'Public Subnet B\n10.0.2.0/24', fontsize=9, color='black', fontweight='bold')
    
    # Private Subnets - App Tier
    priv_app1 = FancyBboxPatch((2, 5.5), 5, 1.5, 
                               boxstyle="round,pad=0.05", 
                               facecolor=colors['private_orange'], 
                               edgecolor='black', alpha=0.3)
    ax.add_patch(priv_app1)
    ax.text(2.2, 6.7, 'Private Subnet A (App)\n10.0.3.0/24', fontsize=9, color='black', fontweight='bold')
    
    priv_app2 = FancyBboxPatch((9, 5.5), 5, 1.5, 
                               boxstyle="round,pad=0.05", 
                               facecolor=colors['private_orange'], 
                               edgecolor='black', alpha=0.3)
    ax.add_patch(priv_app2)
    ax.text(9.2, 6.7, 'Private Subnet B (App)\n10.0.4.0/24', fontsize=9, color='black', fontweight='bold')
    
    # Private Subnets - Database Tier
    priv_db1 = FancyBboxPatch((2, 3.5), 5, 1.5, 
                              boxstyle="round,pad=0.05", 
                              facecolor=colors['database_purple'], 
                              edgecolor='black', alpha=0.3)
    ax.add_patch(priv_db1)
    ax.text(2.2, 4.7, 'Private Subnet A (DB)\n10.0.5.0/24', fontsize=9, color='white', fontweight='bold')
    
    priv_db2 = FancyBboxPatch((9, 3.5), 5, 1.5, 
                              boxstyle="round,pad=0.05", 
                              facecolor=colors['database_purple'], 
                              edgecolor='black', alpha=0.3)
    ax.add_patch(priv_db2)
    ax.text(9.2, 4.7, 'Private Subnet B (DB)\n10.0.6.0/24', fontsize=9, color='white', fontweight='bold')
    
    # ECS Services
    # Vote App
    vote_service = FancyBboxPatch((2.5, 5.8), 1.8, 0.6, 
                                  boxstyle="round,pad=0.02", 
                                  facecolor=colors['container_teal'], 
                                  edgecolor='black')
    ax.add_patch(vote_service)
    ax.text(3.4, 6.1, 'Vote App\n(ECS)', fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Result App
    result_service = FancyBboxPatch((9.5, 5.8), 1.8, 0.6, 
                                    boxstyle="round,pad=0.02", 
                                    facecolor=colors['container_teal'], 
                                    edgecolor='black')
    ax.add_patch(result_service)
    ax.text(10.4, 6.1, 'Result App\n(ECS)', fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Worker Service
    worker_service = FancyBboxPatch((5.5, 5.8), 1.8, 0.6, 
                                    boxstyle="round,pad=0.02", 
                                    facecolor=colors['container_teal'], 
                                    edgecolor='black')
    ax.add_patch(worker_service)
    ax.text(6.4, 6.1, 'Worker\n(ECS)', fontsize=8, ha='center', va='center', fontweight='bold')
    
    # ElastiCache Redis
    redis = FancyBboxPatch((2.5, 3.8), 2, 0.6, 
                           boxstyle="round,pad=0.02", 
                           facecolor=colors['cache_red'], 
                           edgecolor='black')
    ax.add_patch(redis)
    ax.text(3.5, 4.1, 'ElastiCache\nRedis', fontsize=8, ha='center', va='center', color='white', fontweight='bold')
    
    # RDS PostgreSQL
    postgres = FancyBboxPatch((9.5, 3.8), 2, 0.6, 
                              boxstyle="round,pad=0.02", 
                              facecolor=colors['database_purple'], 
                              edgecolor='black')
    ax.add_patch(postgres)
    ax.text(10.5, 4.1, 'RDS\nPostgreSQL', fontsize=8, ha='center', va='center', color='white', fontweight='bold')
    
    # CloudWatch
    cloudwatch = FancyBboxPatch((12.5, 5.8), 1.8, 0.6, 
                                boxstyle="round,pad=0.02", 
                                facecolor=colors['monitoring'], 
                                edgecolor='black')
    ax.add_patch(cloudwatch)
    ax.text(13.4, 6.1, 'CloudWatch\nLogs/Metrics', fontsize=8, ha='center', va='center', fontweight='bold')
    
    # ECR
    ecr = FancyBboxPatch((12.5, 7.8), 1.8, 0.6, 
                         boxstyle="round,pad=0.02", 
                         facecolor=colors['aws_orange'], 
                         edgecolor='black')
    ax.add_patch(ecr)
    ax.text(13.4, 8.1, 'ECR\nContainer\nRegistry', fontsize=8, ha='center', va='center', color='white', fontweight='bold')
    
    # NAT Gateways
    nat1 = FancyBboxPatch((4.5, 7.8), 1, 0.4, 
                          boxstyle="round,pad=0.02", 
                          facecolor='orange', 
                          edgecolor='black')
    ax.add_patch(nat1)
    ax.text(5, 8, 'NAT\nGW', fontsize=7, ha='center', va='center', fontweight='bold')
    
    nat2 = FancyBboxPatch((11.5, 7.8), 1, 0.4, 
                          boxstyle="round,pad=0.02", 
                          facecolor='orange', 
                          edgecolor='black')
    ax.add_patch(nat2)
    ax.text(12, 8, 'NAT\nGW', fontsize=7, ha='center', va='center', fontweight='bold')
    
    # Route 53
    route53 = FancyBboxPatch((1, 11), 2, 0.6, 
                             boxstyle="round,pad=0.02", 
                             facecolor=colors['aws_orange'], 
                             edgecolor='black')
    ax.add_patch(route53)
    ax.text(2, 11.3, 'Route 53\nDNS', fontsize=8, ha='center', va='center', color='white', fontweight='bold')
    
    # Certificate Manager
    acm = FancyBboxPatch((13, 11), 2, 0.6, 
                         boxstyle="round,pad=0.02", 
                         facecolor=colors['aws_orange'], 
                         edgecolor='black')
    ax.add_patch(acm)
    ax.text(14, 11.3, 'ACM\nSSL/TLS', fontsize=8, ha='center', va='center', color='white', fontweight='bold')
    
    # Users
    users = FancyBboxPatch((7, 12.5), 2, 0.6, 
                           boxstyle="round,pad=0.02", 
                           facecolor='lightblue', 
                           edgecolor='black')
    ax.add_patch(users)
    ax.text(8, 12.8, '👥 Users', fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Connection arrows
    # Users to Route 53
    ax.annotate('', xy=(2.5, 11.3), xytext=(7, 12.6),
                arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
    
    # Route 53 to ALB
    ax.annotate('', xy=(6.5, 8.9), xytext=(3, 11.2),
                arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
    
    # Internet Gateway to ALB
    ax.annotate('', xy=(8, 9.3), xytext=(8, 10.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='orange'))
    
    # ALB to services
    ax.annotate('', xy=(3.4, 6.4), xytext=(7.5, 8.5),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='purple'))
    ax.annotate('', xy=(10.4, 6.4), xytext=(8.5, 8.5),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='purple'))
    
    # Services to databases
    ax.annotate('', xy=(3.5, 4.4), xytext=(3.4, 5.8),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='red'))
    ax.annotate('', xy=(10.5, 4.4), xytext=(10.4, 5.8),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='purple'))
    ax.annotate('', xy=(4, 4.1), xytext=(6.4, 5.8),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='red'))
    ax.annotate('', xy=(9.5, 4.1), xytext=(6.4, 5.8),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='purple'))
    
    # Services to CloudWatch
    ax.annotate('', xy=(12.5, 6.1), xytext=(7.3, 6.1),
                arrowprops=dict(arrowstyle='->', lw=1, color='green'))
    
    # Legend
    legend_y = 2.5
    ax.text(1.5, legend_y, 'Legend:', fontsize=12, fontweight='bold')
    
    # Legend items
    legend_items = [
        ('Public Subnet', colors['public_green']),
        ('Private App Subnet', colors['private_orange']),
        ('Private DB Subnet', colors['database_purple']),
        ('ECS Services', colors['container_teal']),
        ('Cache/Database', colors['cache_red']),
        ('AWS Services', colors['aws_orange'])
    ]
    
    for i, (label, color) in enumerate(legend_items):
        y_pos = legend_y - 0.3 - (i * 0.25)
        legend_box = FancyBboxPatch((1.5, y_pos-0.05), 0.3, 0.15, 
                                    boxstyle="round,pad=0.02", 
                                    facecolor=color, 
                                    alpha=0.7)
        ax.add_patch(legend_box)
        ax.text(2, y_pos, label, fontsize=9, va='center')
    
    plt.tight_layout()
    return fig

def create_data_flow_diagram():
    """Create a separate data flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Modern Voting App - Data Flow Architecture', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Components
    components = [
        {'name': 'User Browser', 'pos': (2, 8), 'color': 'lightblue'},
        {'name': 'ALB', 'pos': (7, 8), 'color': '#BD10E0'},
        {'name': 'Vote App\n(Flask)', 'pos': (4, 6), 'color': '#50E3C2'},
        {'name': 'Result App\n(Node.js)', 'pos': (10, 6), 'color': '#50E3C2'},
        {'name': 'Redis\n(Queue)', 'pos': (4, 4), 'color': '#D0021B'},
        {'name': 'Worker\n(.NET)', 'pos': (7, 4), 'color': '#50E3C2'},
        {'name': 'PostgreSQL\n(Database)', 'pos': (10, 4), 'color': '#9013FE'},
        {'name': 'CloudWatch\n(Monitoring)', 'pos': (7, 2), 'color': '#B8E986'}
    ]
    
    # Draw components
    for comp in components:
        box = FancyBboxPatch((comp['pos'][0]-0.8, comp['pos'][1]-0.4), 1.6, 0.8,
                             boxstyle="round,pad=0.1",
                             facecolor=comp['color'],
                             edgecolor='black',
                             linewidth=2)
        ax.add_patch(box)
        ax.text(comp['pos'][0], comp['pos'][1], comp['name'],
                ha='center', va='center', fontsize=10, fontweight='bold',
                color='white' if comp['color'] in ['#BD10E0', '#D0021B', '#9013FE'] else 'black')
    
    # Data flow arrows with labels
    flows = [
        {'from': (2, 8), 'to': (7, 8), 'label': '1. HTTP Request', 'color': 'blue'},
        {'from': (7, 8), 'to': (4, 6), 'label': '2. Route to Vote App', 'color': 'green'},
        {'from': (7, 8), 'to': (10, 6), 'label': '2. Route to Result App', 'color': 'green'},
        {'from': (4, 6), 'to': (4, 4), 'label': '3. Queue Vote', 'color': 'red'},
        {'from': (4, 4), 'to': (7, 4), 'label': '4. Process Vote', 'color': 'orange'},
        {'from': (7, 4), 'to': (10, 4), 'label': '5. Store Vote', 'color': 'purple'},
        {'from': (10, 6), 'to': (10, 4), 'label': '6. Read Results', 'color': 'purple'},
        {'from': (10, 6), 'to': (2, 8), 'label': '7. Real-time Updates', 'color': 'blue'},
        {'from': (7, 4), 'to': (7, 2), 'label': 'Logs & Metrics', 'color': 'gray'},
        {'from': (4, 6), 'to': (7, 2), 'label': 'Logs & Metrics', 'color': 'gray'},
        {'from': (10, 6), 'to': (7, 2), 'label': 'Logs & Metrics', 'color': 'gray'}
    ]
    
    for flow in flows:
        ax.annotate('', xy=flow['to'], xytext=flow['from'],
                    arrowprops=dict(arrowstyle='->', lw=2, color=flow['color']))
        
        # Add label
        mid_x = (flow['from'][0] + flow['to'][0]) / 2
        mid_y = (flow['from'][1] + flow['to'][1]) / 2
        ax.text(mid_x, mid_y + 0.2, flow['label'], 
                ha='center', va='bottom', fontsize=8, 
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # Add process description
    process_text = """
Data Flow Process:
1. User submits vote through web interface
2. ALB routes request to Vote App (Flask)
3. Vote App queues vote in Redis
4. Worker processes vote from Redis queue
5. Worker stores processed vote in PostgreSQL
6. Result App reads real-time data from PostgreSQL
7. Result App sends real-time updates to users via WebSocket
8. All components send logs and metrics to CloudWatch
    """
    
    ax.text(0.5, 1.5, process_text, fontsize=10, va='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#F0F8FF', alpha=0.8))
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # Create architecture diagram
    print("🏗️  Generating AWS Architecture Diagram...")
    arch_fig = create_aws_architecture_diagram()
    arch_fig.savefig('/mnt/c/Users/IsaacTandoh/Downloads/isaac_tandoh/example-voting-app-docker/aws-architecture.png', 
                     dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Architecture diagram saved as 'aws-architecture.png'")
    
    # Create data flow diagram
    print("🔄 Generating Data Flow Diagram...")
    flow_fig = create_data_flow_diagram()
    flow_fig.savefig('/mnt/c/Users/IsaacTandoh/Downloads/isaac_tandoh/example-voting-app-docker/data-flow-diagram.png', 
                     dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Data flow diagram saved as 'data-flow-diagram.png'")
    
    print("\n🎉 Architecture diagrams generated successfully!")
    print("📁 Files created:")
    print("   - aws-architecture.png (AWS infrastructure layout)")
    print("   - data-flow-diagram.png (Application data flow)")
