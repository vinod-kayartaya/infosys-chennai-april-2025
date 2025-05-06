# Jenkins Lab Exercises - Day 1

## Basic Jenkins Jobs

### Prerequisites

- Jenkins server up and running
- Git installed and configured
- Basic understanding of build tools (Maven/Gradle)
- A GitHub account

### Lab Exercise 1: Creating a Basic Freestyle Project

**Objective:** Create a freestyle project that checks out code from a Git repository and runs basic shell commands.

**Steps:**

1. Create a new freestyle project named "hello-world-freestyle"
2. Configure Git repository: https://github.com/your-username/hello-world
3. Add a build step using "Execute shell" with the following commands:
   ```bash
   echo "Hello from Jenkins!"
   date
   pwd
   ls -la
   ```
4. Save and run the build
5. Examine the console output
6. Add a post-build action to archive the workspace files

**Success Criteria:**

- Build completes successfully
- Console output shows the executed commands
- Workspace files are archived

### Lab Exercise 2: Pipeline Project with Jenkinsfile

**Objective:** Create a pipeline project that uses a Jenkinsfile to define the build process.

**Steps:**

1. Create a new pipeline project named "simple-pipeline"
2. Create a Jenkinsfile with the following stages:
   - Checkout
   - Build
   - Test
   - Report
3. Configure the pipeline to use SCM for the Jenkinsfile
4. Run the pipeline and observe the Stage View
5. Add parallel execution in the Test stage

**Success Criteria:**

- Pipeline executes all stages successfully
- Stage View shows the pipeline progress
- Test stage runs parallel tasks

### Lab Exercise 3: Configuring Build Triggers

**Objective:** Set up different types of build triggers for a Jenkins job.

**Steps:**

1. Create a new freestyle project named "scheduled-build"
2. Configure the following build triggers:
   - Poll SCM (every 15 minutes)
   - Build periodically (twice daily)
   - GitHub webhook trigger
3. Add a simple build step
4. Test each trigger type
5. Monitor build history

**Success Criteria:**

- Job builds automatically based on schedule
- SCM polling works correctly
- Webhook trigger responds to GitHub events

### Lab Exercise 4: Working with Build Parameters

**Objective:** Create a parameterized build job that accepts different types of parameters.

**Steps:**

1. Create a new freestyle project named "param-build"
2. Add the following parameters:
   - String parameter: ENVIRONMENT (dev/qa/prod)
   - Choice parameter: BUILD_TYPE (full/incremental)
   - Boolean parameter: SKIP_TESTS
   - Password parameter: API_KEY
3. Use these parameters in shell commands
4. Create a conditional build step based on parameters
5. Test the build with different parameter combinations

**Success Criteria:**

- Build accepts all parameter types
- Parameters are correctly used in build steps
- Conditional execution works based on parameters

### Lab Exercise 5: Job Configuration and Build Environment

**Objective:** Configure advanced job settings and build environment options.

**Steps:**

1. Create a new freestyle project named "advanced-config"
2. Configure the following:
   - Custom workspace
   - Build retention policy (keep max 10 builds)
   - Build environment with:
     - Timestamps in console output
     - Build timeout
     - Environment variables
3. Add build failure conditions
4. Configure email notifications
5. Test the configuration settings

**Success Criteria:**

- Job uses custom workspace
- Old builds are properly cleaned up
- Build environment settings work as expected
- Notifications are sent on build status changes

### Notes

- Document any issues encountered during the exercises
- Take screenshots of important configurations
- Keep track of successful and failed attempts
- Be prepared to explain your configuration choices

### Additional Challenges

- Try combining multiple concepts from different exercises
- Experiment with different plugin configurations
- Create dependencies between jobs
- Implement error handling in your builds

---

_Note: Replace `your-username` with your actual GitHub username when following these exercises._
