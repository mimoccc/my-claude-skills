---
name: kmp-install-tasks
description: Use when setting up or working on any KMP project with Android/Desktop targets. Every such project must have root gradle tasks installAndroid (release APK via adb to the connected device) and installDesktop (desktop distributable installed for the local user). Add them if missing.
---

# Install tasks for KMP projects

Every KMP project with an Android and/or Desktop target gets these two root-level
gradle tasks. When you touch a KMP project that lacks them, add them (group them
with the project's other convenience tasks; psippr uses group `mjdev`).

## installAndroid

Always installs the **release** APK (not debug) to the connected device:

```kotlin
val installAndroid = tasks.register<Exec>("installAndroid") {
    group = "<project group>"
    description = "Installs the release APK to the connected device via adb install -r."
    dependsOn(":androidApp:assembleRelease")
    val adb =
        System.getenv("ANDROID_HOME")?.let { "$it/platform-tools/adb" }
            ?: "${System.getProperty("user.home")}/Android/Sdk/platform-tools/adb"
    commandLine(adb, "install", "-r", rootDir.resolve("androidApp/build/outputs/apk/release/<module>-release.apk").absolutePath)
}
```

Adjust the module path to the project's android module. `adb install -r` keeps
app data; it fails if the installed app has a different signature — never work
around that with uninstall without the user's explicit consent (data loss).

## installDesktop

Installs the current-OS desktop distributable for the local user, no sudo:

- **Linux**: single-file AppImage → `~/.local/bin/<App>.AppImage` (executable),
  icon → `~/.local/share/icons/hicolor/512x512/apps/`, `.desktop` launcher →
  `~/.local/share/applications/` (Exec = the AppImage path). If the project has
  no AppImage pipeline, use the jpackage app-image dir and symlink its launcher
  into `~/.local/bin` instead.
- **macOS**: copy the built `.app` into `~/Applications`.
- **Windows**: run the built MSI/EXE installer per-user.

psippr reference implementation lives in the root `build.gradle.kts`
(`installDesktop`, depends on `packageAppImageFile`).

## IntelliJ IDEA run actions (.run folder)

Both tasks also get committed run configurations in the project's `.run/`
folder (`installAndroid.run.xml`, `installDesktop.run.xml`) so they appear in
the IDE's run-configuration dropdown. Template (GradleRunConfiguration):

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="<taskName>" type="GradleRunConfiguration" factoryName="Gradle">
    <ExternalSystemSettings>
      <option name="executionName" />
      <option name="externalProjectPath" value="$PROJECT_DIR$" />
      <option name="externalSystemIdString" value="GRADLE" />
      <option name="scriptParameters" value="" />
      <option name="taskDescriptions"><list /></option>
      <option name="taskNames"><list><option value="<taskName>" /></list></option>
      <option name="vmOptions" />
    </ExternalSystemSettings>
    <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
    <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
    <ExternalSystemDebugDisabled>false</ExternalSystemDebugDisabled>
    <DebugAllEnabled>false</DebugAllEnabled>
    <RunAsTest>false</RunAsTest>
    <method v="2" />
  </configuration>
</component>
```

If the project already has other `.run/*.run.xml` gradle configs, copy one and
swap the task name instead of using this template.

## Rules

- `installAndroid` is always RELEASE — debug installs are done explicitly via
  `:androidApp:installDebug`, not through this task.
- Keep both tasks configuration-cache compatible: resolve env/paths at
  configuration time into plain values; no `project` access inside `doLast`.
- The tasks must not be wired into build/CI flows — they are developer
  conveniences invoked manually.
