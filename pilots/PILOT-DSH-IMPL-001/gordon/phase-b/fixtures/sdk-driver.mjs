// Gordon G7-14 driver: drive one routed turn through the BUILT TypeScript SDK
// client (@deepseek-ai/dsh-sdk-client) against the dsh-jsonrpc-agent runtime.
// argv: <sdkClientLib> <runtimeBinJs> <cordisConfig> <provider> <model> <task>
// stdout: one JSON result line (marker result, session id, counts, exit path).
import { pathToFileURL } from 'node:url'

const [sdkClientLib, runtimeBinJs, cordisConfig, provider, model, task] =
  process.argv.slice(2)

const { DeepSeekHarness } = await import(pathToFileURL(sdkClientLib).href)

const harness = new DeepSeekHarness({
  launch: { command: process.execPath, args: [runtimeBinJs, cordisConfig] },
  provider,
  model,
})

let result = null
let runError = null
let closeError = null
try {
  result = await harness.run(task)
} catch (error) {
  runError = String(error && error.stack ? error.stack : error)
} finally {
  try {
    await harness.close()
  } catch (error) {
    closeError = String(error)
  }
}

process.stdout.write(JSON.stringify({
  sessionId: result ? result.sessionId : null,
  finalResponse: result ? result.finalResponse : null,
  eventCount: result && Array.isArray(result.events) ? result.events.length : null,
  notificationCount: result && Array.isArray(result.notifications) ? result.notifications.length : null,
  runError,
  closeError,
}) + '\n')
