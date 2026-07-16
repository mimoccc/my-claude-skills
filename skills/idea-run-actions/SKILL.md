---
name: idea-run-actions
description: Use in ANY project whenever a runnable thing exists or is created — a gradle task, shell script, dev server, tool invocation, or recurring command. Whenever possible expose it as an IntelliJ IDEA run action (.run/*.run.xml in the repo) and keep existing run actions working; the user drives projects from the IDE, not the terminal.
---

# IntelliJ IDEA run actions everywhere

The user works from IntelliJ IDEA / Android Studio. Anything runnable that a
human might want to trigger again must be reachable as a **run configuration**
in the IDE — not only as a terminal command buried in a chat log.

## Rules

1. **When you create something runnable** (a gradle task, a script in
   `scripts/`, a dev/build/release helper, a pairing or maintenance command),
   ALSO add a matching run action under `.run/<name>.run.xml` in the repo root,
   committed with the feature. One action per file, `name` = the task/script name.
2. **When a runnable thing already exists without a run action**, add the run
   action while you're touching that area (non-invasively, same commit only if
   it belongs to the change).
3. **When you change or rename a task/script**, update its `.run` file in the
   same commit — a broken run action is worse than none.
4. **Prefer executing via the same entrypoint** the run action uses (same
   gradle task / script), so IDE behavior and agent behavior never diverge.
5. Do NOT create run actions for one-off debugging commands or things that make
   no sense to repeat from the IDE.

## Templates

Gradle task (`.run/<task>.run.xml`):

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="TASK_NAME" type="GradleRunConfiguration" factoryName="Gradle">
    <ExternalSystemSettings>
      <option name="executionName" />
      <option name="externalProjectPath" value="$PROJECT_DIR$" />
      <option name="externalSystemIdString" value="GRADLE" />
      <option name="scriptParameters" value="" />
      <option name="taskDescriptions"><list /></option>
      <option name="taskNames">
        <list><option value="TASK_NAME" /></list>
      </option>
      <option name="vmOptions" />
    </ExternalSystemSettings>
    <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
    <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
    <ExternalSystemDebugDisabled>false</ExternalSystemDebugDisabled>
    <method v="2" />
  </configuration>
</component>
```

Shell script (`.run/<name>.run.xml>`; runs in the IDE terminal so prompts/QR
codes work):

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="NAME" type="ShConfigurationType">
    <option name="SCRIPT_TEXT" value="" />
    <option name="INDEPENDENT_SCRIPT_PATH" value="false" />
    <option name="SCRIPT_PATH" value="$PROJECT_DIR$/scripts/SCRIPT.sh" />
    <option name="SCRIPT_OPTIONS" value="" />
    <option name="INDEPENDENT_SCRIPT_WORKING_DIRECTORY" value="false" />
    <option name="SCRIPT_WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="INDEPENDENT_INTERPRETER_PATH" value="true" />
    <option name="INTERPRETER_PATH" value="/bin/bash" />
    <option name="INTERPRETER_OPTIONS" value="" />
    <option name="EXECUTE_IN_TERMINAL" value="true" />
    <option name="EXECUTE_SCRIPT_FILE" value="true" />
    <envs />
    <method v="2" />
  </configuration>
</component>
```

Reference examples live in psippr `.run/` (installAndroid, installDesktop,
whatsappPair, buildAll). See also [[kmp-install-tasks]] and
[[kmp-whatsapp-release]] — their tasks/scripts must always ship with run
actions.
