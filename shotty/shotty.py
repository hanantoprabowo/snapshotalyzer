import boto3
import botocore
import click


def get_ec2_resource(profile, region):
	session = boto3.Session(profile_name=profile, region_name=region)
	return session.resource('ec2')

def filter_instances(ec2, project=None, instance=None):
	filters = []
	
	if project:
		filters.append({'Name':'tag:Project', 'Values':[project]})
	
	if instance:
		filters.append({'Name':'instance-id', 'Values':[instance]})
	
	return ec2.instances.filter(Filters=filters)
		
def has_pending_snapshot(volume):
	snapshots = list(volume.snapshots.all())
	return snapshots and snapshots[0].state == 'pending'
	
@click.group()
@click.option('--profile', default='shotty', 
	help="Specify a profile (default: 'shotty')")
@click.option('--region', default=None,
	help="Specify a region")
@click.pass_context
def cli(ctx, profile, region):
	"""Shotty manages snapshots"""
	
	ctx.ensure_object(dict)
	ctx.obj['PROFILE'] = profile
	ctx.obj['REGION'] = region

@cli.group()
def snapshots():
	"""Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None, 
	help="Only snapshots for project (tag Project:<name>)")
@click.option('--instance', default=None, 
	help="Only snapshots for the specified instance")
@click.option('--all', 'list_all', default=False, is_flag=True,
	help="List all snapshots for each volume, not just the most recent")
@click.pass_context
def list_snapshots(ctx, project, instance, list_all):
	"List EC2 snapshots"
	
	ec2 = get_ec2_resource(ctx.obj['PROFILE'], ctx.obj['REGION'])
	instances = filter_instances(ec2, project, instance)
	
	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshots.all():			
				print(', '.join((
					s.id,
					v.id,
					i.id,
					s.state,
					s.progress,
					s.start_time.strftime("%c")
				)))
	
				if s.state == 'completed' and not list_all: break
	
	return

@cli.group()
def volumes():
	"""Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None, 
	help="Only volumes for project (tag Project:<name>)")
@click.option('--instance', default=None, 
	help="Only volumes for the specified instance")
@click.pass_context
def list_volumes(ctx, project, instance):
	"List EC2 volumes"
	
	ec2 = get_ec2_resource(ctx.obj['PROFILE'], ctx.obj['REGION'])
	instances = filter_instances(ec2, project, instance)
	
	for i in instances:
		for v in i.volumes.all():
			print(', '.join((
				v.id,
				i.id,
				v.state,
				str(v.size) + "GiB",
				v.encrypted and "Encrypted" or "Not Encrypted"
			)))
	
	return
	
@cli.group()
def instances():
	"""Commands for instances"""

@instances.command('snapshot')
@click.option('--project', default=None, 
	help="Only instances for project (tag Project:<name>)")
@click.option('--instance', default=None, 
	help="Only for the specified instance")
@click.option('--force', 'force', default=False, is_flag=True,
	help="Force to snapshot instances")
@click.pass_context
def create_snapshots(ctx, project, instance, force):
	"Create snapshots for EC2 instances"
	
	if not (project or instance or force):
		print("Neither --project nor --instance nor --force is defined. Operation aborted.")
		return
	
	ec2 = get_ec2_resource(ctx.obj['PROFILE'], ctx.obj['REGION'])
	instances = filter_instances(ec2, project, instance)
	
	for i in instances:
		print("Stopping {0}...".format(i.id))
		old_state = i.state['Name']
		
		i.stop()
		i.wait_until_stopped()
		
		for v in i.volumes.all():
			if has_pending_snapshot(v):
				print("  Skipping {0}, snapshot already in progress".format(v.id))
				continue

			print("  Creating snapshot of {0}".format(v.id))
			
			try:
				v.create_snapshot(Description="Created by Snapshotalyzer")
			except botocore.exceptions.ClientError as e:
				print("  Could not snapshot {0}. ".format(v.id) + str(e))
				continue
		
		if old_state == 'running':
			print("Starting {0}...".format(i.id))
		
			i.start()
			i.wait_until_running()
		
	print("Job's done")
	
	return


@instances.command('list')
@click.option('--project', default=None, 
	help="Only instances for project (tag Project:<name>)")
@click.option('--instance', default=None, 
	help="Only for the specified instance")
@click.pass_context
def list_instances(ctx, project, instance):
	"List EC2 instances"
	
	ec2 = get_ec2_resource(ctx.obj['PROFILE'], ctx.obj['REGION'])
	instances = filter_instances(ec2, project, instance)
	
	for i in instances:
		tags = { t['Key']: t['Value'] for t in i.tags or [] }
		print(', '.join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,
			tags.get('Project','<no project>')
			)))
	
	return

@instances.command('stop')
@click.option('--project', default=None, 
	help="Only instances for project (tag Project:<name>)")
@click.option('--instance', default=None, 
	help="Only for the specified instance")
@click.option('--force', 'force', default=False, is_flag=True,
	help="Force to stop instances")
@click.pass_context
def stop_instances(ctx, project, instance, force):
	"Stop EC2 instances"
	
	if not (project or instance or force):
		print("Neither --project nor --instance nor --force is defined. Operation aborted.")
		return
	
	ec2 = get_ec2_resource(ctx.obj['PROFILE'], ctx.obj['REGION'])
	instances = filter_instances(ec2, project, instance)
	
	for i in instances:
		print("Stopping {0}...".format(i.id))
		try:
			i.stop()
		except botocore.exceptions.ClientError as e:
			print(" Could not stop {0}. ".format(i.id) + str(e))
			continue
	
	return

@instances.command('start')
@click.option('--project', default=None, 
	help="Only instances for project (tag Project:<name>)")
@click.option('--instance', default=None, 
	help="Only for the specified instance")
@click.option('--force', 'force', default=False, is_flag=True,
	help="Force to start instances")
@click.pass_context
def start_instances(ctx, project, instance, force):
	"Start EC2 instances"
	
	if not (project or instance or force):
		print("Neither --project nor --instance nor --force is defined. Operation aborted.")
		return
	
	ec2 = get_ec2_resource(ctx.obj['PROFILE'], ctx.obj['REGION'])
	instances = filter_instances(ec2, project, instance)
	
	for i in instances:
		print("Starting {0}...".format(i.id))
		try:
			i.start()
		except botocore.exceptions.ClientError as e:
			print(" Could not start {0}. ".format(i.id) + str(e))
			continue
	
	return

@instances.command('reboot')
@click.option('--project', default=None, 
	help="Only instances for project (tag Project:<name>)")
@click.option('--instance', default=None, 
	help="Only for the specified instance")
@click.option('--force', 'force', default=False, is_flag=True,
	help="Force to reboot instances")
@click.pass_context
def reboot_instances(ctx, project, instance, force):
	"Reboot EC2 instances"
	
	if not (project or instance or force):
		print("Neither --project nor --instance nor --force is defined. Operation aborted.")
		return
	
	ec2 = get_ec2_resource(ctx.obj['PROFILE'], ctx.obj['REGION'])
	instances = filter_instances(ec2, project, instance)
	
	for i in instances:
		print("Rebooting {0}...".format(i.id))
		try:
			i.reboot()
		except botocore.exceptions.ClientError as e:
			print(" Could not reboot {0}. ".format(i.id) + str(e))
			continue
	
	return

if __name__ == '__main__':
	cli(obj={})