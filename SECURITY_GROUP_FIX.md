# AWS Security Group - Duplicate Rule Error Fix

## Problem
> "A security group rule with the same protocol, port range, and source has already been added to this security group."

This means you're trying to add a rule that already exists.

---

## Solution 1: Check Existing Rules (Console)

1. **AWS Console** → EC2 → Security Groups
2. Find your security group: `churnguard-sg`
3. Click on it
4. Go to **Inbound rules** tab
5. Look for existing rules:
   - SSH (Port 22)
   - HTTP (Port 80)
   - HTTPS (Port 443)

If any already exist, **skip adding them again**.

---

## Solution 2: Delete Duplicate Rule

1. **Inbound rules** tab
2. Find the duplicate rule
3. Click the **X** button on the right side
4. Click **Delete**
5. Then add the correct rule

---

## Solution 3: Create Fresh Security Group

If rules are messed up, start fresh:

### Step 1: Delete Old Group
1. EC2 → Security Groups
2. Select `churnguard-sg`
3. Click **Delete security group**
4. Confirm

### Step 2: Create New Group
1. Click **Create security group**
2. **Name**: `churnguard-sg-v2`
3. **Description**: ChurnGuard security group
4. **VPC**: Default VPC

### Step 3: Add Rules Carefully (One at a Time)

**Rule 1 - SSH:**
- Type: SSH
- Protocol: TCP
- Port: 22
- Source: 0.0.0.0/0 (or your IP for security)
- Click **Add rule**

**Rule 2 - HTTP:**
- Type: HTTP
- Protocol: TCP
- Port: 80
- Source: 0.0.0.0/0
- Click **Add rule**

**Rule 3 - HTTPS:**
- Type: HTTPS
- Protocol: TCP
- Port: 443
- Source: 0.0.0.0/0
- Click **Add rule**

Then click **Create security group**

---

## Solution 4: AWS CLI (Fastest)

If you have AWS CLI installed:

```bash
# Create fresh security group
aws ec2 create-security-group \
  --group-name churnguard-sg \
  --description "ChurnGuard security group" \
  --query 'GroupId'

# Note the GroupId returned (e.g., sg-0123456789abcdef)

# Add SSH rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-XXXXXXXXX \
  --protocol tcp --port 22 \
  --cidr 0.0.0.0/0

# Add HTTP rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-XXXXXXXXX \
  --protocol tcp --port 80 \
  --cidr 0.0.0.0/0

# Add HTTPS rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-XXXXXXXXX \
  --protocol tcp --port 443 \
  --cidr 0.0.0.0/0
```

Replace `sg-XXXXXXXXX` with your actual GroupId.

---

## Solution 5: Use Existing Security Group

If you already have a working security group, just use that:

1. When launching instance, select **Choose existing security group**
2. Pick an existing group with SSH, HTTP, HTTPS enabled
3. Proceed with launch

---

## Correct Final Rules

Your security group should have **exactly 3 inbound rules**:

| Type | Protocol | Port Range | Source |
|------|----------|-----------|--------|
| SSH | TCP | 22 | 0.0.0.0/0 |
| HTTP | TCP | 80 | 0.0.0.0/0 |
| HTTPS | TCP | 443 | 0.0.0.0/0 |

If you have more than 3, or duplicates, delete the extras.

---

## Next Steps

Once security group is fixed:

1. **Launch EC2 instance** with the corrected security group
2. **Wait for instance to start** (1-2 minutes)
3. Copy the **Public IPv4 address**
4. Proceed with deployment

---

## Still Having Issues?

Try this quick fix:

```bash
# Delete the problematic security group (if not in use)
aws ec2 delete-security-group --group-name churnguard-sg

# Then create a brand new one with the 3 rules
# (See Solution 3 or 4 above)
```

Let me know once security group is fixed and instance is running!
