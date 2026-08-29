# WORK ORDER — Chris: lane verification on hxs-9 PostgreSQL

You are Chris, PostgreSQL DBA. Your model lane was just changed to DeepSeek V4 Pro via Baidu FP8. This is a capability test — can you connect to the database and run a query?

## Task

1. SSH to hxsa@192.168.50.208. The SSH password is in /home/hxsa/opt/local-tkv/agent-zero-docs/.local.env (HX_SSH_PASSWORD). Use a temp askpass helper (mode 0700), delete it after.

2. Connect to PostgreSQL on hxs-9:
   `sudo -u postgres psql -c "SELECT version();"`

3. Run a second query to prove read access:
   `sudo -u postgres psql -c "SELECT datname FROM pg_database WHERE datistemplate = false;"`

4. Run a third query to show the roles you created in Step 2:
   `sudo -u postgres psql -c "SELECT rolname, rolcanlogin FROM pg_roles WHERE rolname LIKE 'ps-%' ORDER BY rolname;"`

5. Paste all three outputs.

6. Clean up the askpass helper.

That's it. No mutations. Just prove you can connect and query.
