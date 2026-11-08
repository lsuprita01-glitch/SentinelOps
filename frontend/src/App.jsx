
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Shield, LayoutDashboard, Activity, Network, BrainCircuit, Clock3,
  FlaskConical, Database, ChartNoAxesCombined, Settings, Search, Bell,
  ChevronDown, ArrowUpRight, Zap, LockKeyhole, Radio, Play, RefreshCw,
  CheckCircle2, AlertTriangle, Menu, Eye, Bot, Globe2, Crosshair,
  ShieldCheck, Sparkles, GitBranch, History, FileSearch, Gauge,
  Terminal, Fingerprint, Server
} from "lucide-react";
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip,
  CartesianGrid, BarChart, Bar
} from "recharts";
import ThreatGlobe from "./ThreatGlobe";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const WS_URL = import.meta.env.VITE_WS_URL || "ws://127.0.0.1:8000/ws/events";

const navigation = [
  { name: "Command Centre", icon: LayoutDashboard },
  { name: "Live Threat Monitor", icon: Activity },
  { name: "AI War Room", icon: BrainCircuit },
  { name: "Attack Chain Predictor", icon: Network },
  { name: "Cyberattack Time Machine", icon: Clock3 },
  { name: "What-If Simulator", icon: FlaskConical },
  { name: "Memory Vault", icon: Database },
  { name: "Learning Analytics", icon: ChartNoAxesCombined }
];

const agents = [
  { name: "Detective", role: "Investigates incident evidence", icon: Eye, color: "cyan" },
  { name: "Memory", role: "Recalls historical incidents", icon: BrainCircuit, color: "purple" },
  { name: "Prediction", role: "Forecasts possible attack stages", icon: Network, color: "green" },
  { name: "Response Strategist", role: "Plans defensive responses", icon: ShieldCheck, color: "blue" },
  { name: "Auditor", role: "Checks safety and evidence", icon: LockKeyhole, color: "orange" },
  { name: "Cross-Incident", role: "Connects related incidents", icon: Database, color: "pink" }
];

const trendData = [
  { time: "09:00", events: 12, threats: 3 },
  { time: "09:30", events: 18, threats: 5 },
  { time: "10:00", events: 14, threats: 2 },
  { time: "10:30", events: 29, threats: 9 },
  { time: "11:00", events: 23, threats: 6 },
  { time: "11:30", events: 38, threats: 12 },
  { time: "12:00", events: 26, threats: 7 }
];

const severityData = [
  { name: "Critical", count: 2 },
  { name: "High", count: 8 },
  { name: "Medium", count: 14 },
  { name: "Low", count: 23 }
];

const startingEvents = [
  { id: "EVT-001", time: "10:42:08", type: "Login failures", source: "192.0.2.45", severity: "HIGH" },
  { id: "EVT-002", time: "10:41:52", type: "Authentication event", source: "192.0.2.80", severity: "LOW" },
  { id: "EVT-003", time: "10:40:31", type: "Login failures", source: "192.0.2.45", severity: "MEDIUM" },
  { id: "EVT-004", time: "10:39:14", type: "Access attempt", source: "192.0.2.18", severity: "LOW" }
];

function Metric({ label, value, detail, icon: Icon, color }) {
  return (
    <motion.div
      className="metric-card glass-card"
      whileHover={{ y: -5, scale: 1.015 }}
      transition={{ duration: 0.2 }}
    >
      <div className="metric-top">
        <span>{label}</span>
        <div className={`metric-icon ${color}`}>
          <Icon size={19} />
        </div>
      </div>
      <div className="metric-value">{value}</div>
      <div className="metric-detail">
        <span className="metric-change">
          <ArrowUpRight size={14} /> {detail}
        </span>
        <span>demo indicator</span>
      </div>
    </motion.div>
  );
}

function Panel({ title, subtitle, icon: Icon, children, className = "" }) {
  return (
    <section className={`panel glass-card ${className}`}>
      <div className="panel-heading">
        <div>
          {Icon && (
            <div className="section-kicker">
              <Icon size={13} /> SENTINELOPS INTELLIGENCE
            </div>
          )}
          <h2>{title}</h2>
          {subtitle && <p>{subtitle}</p>}
        </div>
      </div>
      {children}
    </section>
  );
}

function DataRow({ label, value, status = "verified" }) {
  return (
    <div className="incident-status-row">
      <span>{label}</span>
      <strong className={status}>{value}</strong>
    </div>
  );
}

function PageContent({
  page,
  events,
  latestIncident,
  report,
  warRoomStatus,
  runDemoIncident,
  busy
}) {
  const eventTable = (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>EVENT ID</th>
            <th>TIME</th>
            <th>EVENT</th>
            <th>SOURCE</th>
            <th>SEVERITY</th>
          </tr>
        </thead>
        <tbody>
          {events.slice(0, 8).map(event => (
            <tr key={event.id}>
              <td className="event-id">{event.id}</td>
              <td>{event.time}</td>
              <td>{event.type}</td>
              <td className="source-ip">{event.source}</td>
              <td>
                <span className={`severity-badge ${String(event.severity).toLowerCase()}`}>
                  {event.severity}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  if (page === "Command Centre") {
    return (
      <>
        <section className="hero-visual-panel">
          <div className="hero-grid-overlay" />

          <div className="hero-visual-content">
            <div className="eyebrow">
              <Sparkles size={14} /> NEXT-GENERATION CYBER INTELLIGENCE
            </div>

            <h2>
              Detect. Remember.
              <br />
              <span>Predict. Defend. Evolve.</span>
            </h2>

            <p>
              A self-learning AI security command centre that transforms
              incident history into stronger future defence.
            </p>

            <div className="hero-stats">
              <div><strong>06</strong><span>AI SPECIALISTS</span></div>
              <div><strong>24/7</strong><span>MONITORING DESIGN</span></div>
              <div><strong>∞</strong><span>LEARNING CYCLE</span></div>
            </div>

            <div className="hero-footnote">
              <span className="pulse-dot" />
              HINDSIGHT-POWERED INTELLIGENCE
            </div>
          </div>

          <div className="hero-globe-container">
            <div className="globe-orbit-label label-one">
              <Crosshair size={12} /> THREAT INTELLIGENCE
            </div>
            <div className="globe-orbit-label label-two">
              <Globe2 size={12} /> GLOBAL NETWORK VIEW
            </div>
            <ThreatGlobe />
            <div className="globe-center-caption">
              <span className="pulse-dot" /> SENTINEL NETWORK
            </div>
          </div>
        </section>

        <section className="metrics-grid">
          <Metric label="Events monitored" value="1,284" detail="Illustrative" icon={Activity} color="blue" />
          <Metric label="Threat signals" value="24" detail="Illustrative" icon={Shield} color="red" />
          <Metric label="Incidents analysed" value="18" detail="Illustrative" icon={Eye} color="purple" />
          <Metric label="Memory records" value="156" detail="Illustrative" icon={BrainCircuit} color="green" />
        </section>

        <section className="dashboard-grid">
          <Panel title="Threat activity" subtitle="Illustrative activity trend · sample data">
            <div className="chart-area">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trendData}>
                  <defs>
                    <linearGradient id="eventsFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#28c9f3" stopOpacity={0.3} />
                      <stop offset="100%" stopColor="#28c9f3" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="#233449" strokeDasharray="3 5" vertical={false} />
                  <XAxis dataKey="time" stroke="#71869e" />
                  <YAxis stroke="#71869e" />
                  <Tooltip />
                  <Area type="monotone" dataKey="events" stroke="#28c9f3" fill="url(#eventsFill)" />
                  <Area type="monotone" dataKey="threats" stroke="#a58aff" fill="#a58aff" fillOpacity={0.12} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Panel>

          <Panel title="Threat severity" subtitle="Illustrative distribution">
            <div className="severity-chart">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={severityData} layout="vertical">
                  <XAxis type="number" hide />
                  <YAxis type="category" dataKey="name" stroke="#9aabc0" width={65} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#35c8ed" radius={[0, 5, 5, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Panel>
        </section>

        <Panel title="Latest incident" subtitle="Most recent submitted investigation" icon={ShieldCheck}>
          {latestIncident ? (
            <>
              <DataRow label="Incident ID" value={latestIncident.incident_id} />
              <DataRow label="Type" value={latestIncident.type} />
              <DataRow label="Failed attempts" value={latestIncident.failed_attempts} />
              <DataRow label="War Room" value={warRoomStatus} />
              {report && <DataRow label="Investigation" value="Completed" />}
            </>
          ) : (
            <div className="empty-incident">
              <Shield size={28} />
              <strong>No incident submitted yet</strong>
              <span>Launch a demo investigation to begin.</span>
            </div>
          )}
        </Panel>
      </>
    );
  }

  if (page === "Live Threat Monitor") {
    return (
      <>
        <section className="metrics-grid">
          <Metric label="Events in current feed" value={events.length} detail="WebSocket feed" icon={Activity} color="blue" />
          <Metric label="High severity events" value={events.filter(e => e.severity === "HIGH" || e.severity === "CRITICAL").length} detail="Current sample" icon={AlertTriangle} color="red" />
          <Metric label="Feed status" value="LIVE" detail="Connection state shown above" icon={Radio} color="green" />
          <Metric label="Displayed records" value={Math.min(events.length, 8)} detail="Latest events" icon={Database} color="purple" />
        </section>

        <Panel title="Live security event stream" subtitle="Events arriving from the backend WebSocket connection" icon={Radio}>
          {eventTable}
          <p className="panel-bottom-note">
            The initial rows are illustrative. Connect an authorised log source before treating events as real telemetry.
          </p>
        </Panel>

        <Panel title="Monitoring notes" subtitle="How to interpret this feed">
          <DataRow label="Data source" value="Backend WebSocket" />
          <DataRow label="Current demo mode" value="Synthetic events" />
          <DataRow label="Automated containment" value="Disabled · human approval required" status="warning" />
        </Panel>
      </>
    );
  }

  if (page === "AI War Room") {
    return (
      <>
        <Panel title="Multi-agent incident response" subtitle="Six specialist agents coordinated by the SentinelOps orchestrator" icon={BrainCircuit}>
          <div className="agent-network">
            <div className="network-core">
              <Shield size={25} />
              <span>ORCHESTRATOR</span>
            </div>

            <div className="agents-grid">
              {agents.map((agent, index) => {
                const Icon = agent.icon;
                return (
                  <motion.div
                    className="agent-card"
                    key={agent.name}
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.07 }}
                    whileHover={{ y: -4 }}
                  >
                    <div className={`agent-icon ${agent.color}`}>
                      <Icon size={19} />
                    </div>
                    <div className="agent-info">
                      <strong>{agent.name}</strong>
                      <span>{agent.role}</span>
                    </div>
                    <span className="agent-indicator"><i /> READY</span>
                  </motion.div>
                );
              })}
            </div>
          </div>

          <div className="warroom-footer">
            <span><Bot size={15} /> Orchestrator coordinates the six specialist agents</span>
            <span><LockKeyhole size={13} /> Human approval required for sensitive actions</span>
          </div>
        </Panel>

        <Panel title="Investigation console" subtitle="Submit a controlled synthetic incident to start the investigation" icon={Terminal}>
          <div className="incident-details">
            <span className="incident-number">DEMO SCENARIO · INC-TEST</span>
            <h3>Privileged account login anomaly</h3>
            <div className="incident-facts">
              <div><span>Failed attempts</span><strong>38</strong></div>
              <div><span>Time window</span><strong>2 min</strong></div>
              <div><span>Severity</span><strong>High</strong></div>
            </div>
          </div>

          <button className="primary-button" onClick={runDemoIncident} disabled={busy}>
            {busy ? <RefreshCw className="spin" size={15} /> : <Play size={15} />}
            {busy ? "Processing investigation..." : "Run six-agent investigation"}
          </button>

          <DataRow label="Current War Room status" value={warRoomStatus} />
          {report && <pre className="report-output">{JSON.stringify(report, null, 2)}</pre>}
        </Panel>
      </>
    );
  }

  if (page === "Attack Chain Predictor") {
    const stages = [
      { n: "01 · Initial access", d: "Repeated authentication failures observed in the synthetic scenario.", s: "Observed" },
      { n: "02 · Credential access", d: "Check for credential stuffing or password reuse indicators.", s: "Investigate" },
      { n: "03 · Account validation", d: "Look for successful authentication and session creation.", s: "Evidence required" },
      { n: "04 · Privilege misuse", d: "Review privileged actions only if a successful session is confirmed.", s: "Conditional" }
    ];

    return (
      <>
        <Panel title="Attack progression hypothesis" subtitle="Illustrative attack-chain view · stages are hypotheses, not confirmed activity" icon={GitBranch}>
          <div className="agents-grid">
            {stages.map(stage => (
              <div className="agent-card" key={stage.n}>
                <div className="agent-icon cyan"><Network size={18} /></div>
                <div className="agent-info">
                  <strong>{stage.n}</strong>
                  <span>{stage.d}</span>
                </div>
                <span className="agent-indicator">{stage.s}</span>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="Evidence checklist" subtitle="Collect evidence before assigning confidence" icon={FileSearch}>
          <DataRow label="Authentication success records" value="Required" />
          <DataRow label="Identity provider audit trail" value="Required" />
          <DataRow label="Endpoint and session telemetry" value="Recommended" />
          <DataRow label="Privilege-change events" value="Conditional" />
        </Panel>
      </>
    );
  }

  if (page === "Cyberattack Time Machine") {
    const timeline = [
      { t: "T−03:00", h: "Authentication burst begins", d: "Synthetic login failures start against a privileged account." },
      { t: "T−02:00", h: "Detection threshold reached", d: "The demo event engine flags repeated failures within its configured window." },
      { t: "T−01:00", h: "Investigation initiated", d: "Detective and Memory agents review supplied evidence and related memories." },
      { t: "T+00:00", h: "Response recommendation", d: "Strategist proposes defensive checks; Auditor reviews safety and evidence." }
    ];

    return (
      <>
        <Panel title="Incident replay timeline" subtitle="Replay the sequence of a stored demonstration incident" icon={History}>
          <div className="agents-grid">
            {timeline.map((item, index) => (
              <div className="agent-card" key={item.t}>
                <div className="agent-icon purple"><Clock3 size={18} /></div>
                <div className="agent-info">
                  <strong>{item.t} · {item.h}</strong>
                  <span>{item.d}</span>
                </div>
                <span className="agent-indicator">STEP {index + 1}</span>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="Replay controls" subtitle="Demo timeline controls">
          <p>Choose an incident from the Memory Vault when persistent incident records are connected. This visual timeline is an illustrative replay, not a forensic record.</p>
          <button className="primary-button" onClick={runDemoIncident} disabled={busy}>
            <Play size={15} /> Run demo incident again
          </button>
        </Panel>
      </>
    );
  }

  if (page === "What-If Simulator") {
    const scenarios = [
      { n: "Scenario A · Source IP verified", d: "What if the source IP is confirmed in the identity-provider logs?", r: "Consider a narrowly scoped block only after analyst approval." },
      { n: "Scenario B · Successful login found", d: "What if further evidence confirms a successful privileged login?", r: "Escalate investigation, preserve evidence and follow incident policy." },
      { n: "Scenario C · MFA unavailable", d: "What if MFA is not enabled for the affected account?", r: "Recommend identity hardening review; do not change production settings automatically." }
    ];

    return (
      <>
        <Panel title="Isolated what-if scenario lab" subtitle="Explore hypothetical outcomes without touching real systems" icon={FlaskConical}>
          <div className="agents-grid">
            {scenarios.map(scenario => (
              <div className="agent-card" key={scenario.n}>
                <div className="agent-icon blue"><FlaskConical size={18} /></div>
                <div className="agent-info">
                  <strong>{scenario.n}</strong>
                  <span>{scenario.d}<br /><b>{scenario.r}</b></span>
                </div>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="Safety boundary" subtitle="Simulation only">
          <DataRow label="Execution target" value="No production systems" />
          <DataRow label="Real containment" value="Not available" />
          <DataRow label="Approval" value="Required for sensitive actions" status="warning" />
        </Panel>
      </>
    );
  }

  if (page === "Memory Vault") {
    return (
      <>
        <section className="metrics-grid">
          <Metric label="Memory bank" value="ACTIVE" detail="Hindsight connection tested" icon={BrainCircuit} color="purple" />
          <Metric label="Memory categories" value="03" detail="Incidents · actions · outcomes" icon={Database} color="blue" />
          <Metric label="Recall mode" value="Semantic" detail="Relevant past experiences" icon={Search} color="green" />
          <Metric label="Evidence policy" value="Verified" detail="Separate facts from hypotheses" icon={Fingerprint} color="red" />
        </section>

        <Panel title="Incident memory records" subtitle="Example memory structure for retained experiences" icon={Database}>
          <div className="incident-details">
            <span className="incident-number">MEMORY · INC-001</span>
            <h3>Simulated authentication brute-force incident</h3>
            <DataRow label="Observed evidence" value="45 failed attempts in 3 minutes" />
            <DataRow label="Recorded response" value="Simulated source block and MFA enablement" />
            <DataRow label="Recorded outcome" value="No further unauthorised access in the simulation" />
            <DataRow label="Learning" value="Investigate repeated failures and protect the account" />
          </div>
          <p className="panel-bottom-note">
            This is a previously tested synthetic memory example. Hindsight memory is not a substitute for original forensic evidence.
          </p>
        </Panel>
      </>
    );
  }

  if (page === "Learning Analytics") {
    const dimensions = [
      { n: "Recall accuracy · 25%", d: "Did the system retrieve relevant historical incident memories?" },
      { n: "Recommendation quality · 30%", d: "Were recommendations evidence-based, safe and useful?" },
      { n: "Outcome success · 25%", d: "Did the approved response achieve its measured objective?" },
      { n: "Mistake avoidance · 20%", d: "Did the agents avoid unsupported claims and unsafe actions?" }
    ];

    return (
      <>
        <section className="metrics-grid">
          <Metric label="Learning loop" value="DESIGNED" detail="Retain · recall · reflect" icon={BrainCircuit} color="purple" />
          <Metric label="Evaluation dimensions" value="04" detail="Recall · quality · outcome · mistakes" icon={Gauge} color="blue" />
          <Metric label="Benchmark status" value="Pending" detail="Needs measured test runs" icon={ChartNoAxesCombined} color="orange" />
          <Metric label="Evidence integrity" value="Priority" detail="Original evidence preserved separately" icon={ShieldCheck} color="green" />
        </section>

        <Panel title="Sentinel Intelligence Index" subtitle="App-defined evaluation framework · not a native Hindsight score" icon={ChartNoAxesCombined}>
          <div className="agents-grid">
            {dimensions.map(item => (
              <div className="agent-card" key={item.n}>
                <div className="agent-icon green"><CheckCircle2 size={18} /></div>
                <div className="agent-info">
                  <strong>{item.n}</strong>
                  <span>{item.d}</span>
                </div>
              </div>
            ))}
          </div>
          <p className="panel-bottom-note">
            No numerical score is displayed until real benchmark results are collected. Compare memory-enabled and memory-disabled runs using the same test cases.
          </p>
        </Panel>
      </>
    );
  }

  return (
    <Panel title="Workspace" subtitle="Select a command workspace from the navigation." icon={Server} />
  );
}

function pageDescription(page) {
  const descriptions = {
    "Command Centre": "Your adaptive AI cybersecurity command centre.",
    "Live Threat Monitor": "Inspect the incoming event stream and current threat signals.",
    "AI War Room": "Coordinate specialist agents through a safe, evidence-led investigation.",
    "Attack Chain Predictor": "Explore possible next stages and the evidence needed to validate them.",
    "Cyberattack Time Machine": "Replay a demonstration incident and review its response timeline.",
    "What-If Simulator": "Test hypothetical incident scenarios in an isolated simulation.",
    "Memory Vault": "Review retained incident experiences, actions and lessons.",
    "Learning Analytics": "Evaluate whether memory improves future incident response."
  };

  return descriptions[page] || "SentinelOps security workspace.";
}

function App() {
  const [activePage, setActivePage] = useState("Command Centre");
  const [events, setEvents] = useState(startingEvents);
  const [connection, setConnection] = useState("Connecting");
  const [warRoomStatus, setWarRoomStatus] = useState("Idle");
  const [latestIncident, setLatestIncident] = useState(null);
  const [report, setReport] = useState(null);
  const [busy, setBusy] = useState(false);
  const [mobileMenu, setMobileMenu] = useState(false);
  const [notice, setNotice] = useState("");

  useEffect(() => {
    let socket;
    let retry;
    let stopped = false;

    function connect() {
      if (stopped) return;

      try {
        socket = new WebSocket(WS_URL);

        socket.onopen = () => setConnection("Connected");

        socket.onclose = () => {
          setConnection("Disconnected");
          if (!stopped) retry = setTimeout(connect, 3000);
        };

        socket.onerror = () => setConnection("Disconnected");

        socket.onmessage = message => {
          try {
            const payload = JSON.parse(message.data);
            const data = payload.data || {};

            if (payload.type === "event") {
              setEvents(previous => [{
                id: data.event_id || `EVT-${Date.now()}`,
                time: new Date().toLocaleTimeString(),
                type: data.event_type || data.type || "Security event",
                source: data.source_ip || data.ip_address || "Unknown",
                severity: data.severity || "LOW"
              }, ...previous].slice(0, 10));
            }

            if (payload.type === "threat_alert") {
              setLatestIncident(data);
              setWarRoomStatus("Queued");
              setNotice(`Threat alert received: ${data.incident_id || "New incident"}`);
            }

            if (payload.type === "war_room_started") {
              setWarRoomStatus("Running");
              setNotice(`AI War Room started for ${payload.incident_id || "incident"}`);
            }

            if (payload.type === "war_room_completed") {
              setWarRoomStatus("Completed");
              setReport(data);
              setBusy(false);
              setNotice("AI War Room investigation completed.");
            }

            if (payload.type === "war_room_failed") {
              setWarRoomStatus("Failed");
              setBusy(false);
              setNotice(`War Room error: ${payload.error || "Unknown error"}`);
            }
          } catch (error) {
            console.error("WebSocket message error:", error);
          }
        };
      } catch {
        setConnection("Disconnected");
      }
    }

    connect();

    return () => {
      stopped = true;
      clearTimeout(retry);
      if (socket) socket.close();
    };
  }, []);

  async function runDemoIncident() {
    setBusy(true);
    setWarRoomStatus("Submitting");
    setReport(null);
    setNotice("Submitting a synthetic incident to the AI War Room...");

    const incident = {
      incident_id: `INC-${Date.now().toString().slice(-6)}`,
      type: "Suspicious Login Activity",
      attack_type: "Possible Brute Force",
      failed_attempts: 38,
      time_window_minutes: 2,
      target: "Privileged Employee Account",
      unfamiliar_ip: true,
      successful_login: false,
      source_ip: "192.0.2.45",
      environment: "Synthetic Simulation"
    };

    try {
      const response = await fetch(`${API_URL}/alerts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(incident)
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const result = await response.json();
      setLatestIncident(incident);
      setWarRoomStatus("Queued");
      setNotice(result.message || "Incident accepted by SentinelOps.");
      setBusy(false);
    } catch (error) {
      setBusy(false);
      setWarRoomStatus("Offline");
      setNotice(`Backend connection failed: ${error.message}. Check that FastAPI is running.`);
    }
  }

  const online = connection === "Connected";

  return (
    <div className="app-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <aside className={`sidebar ${mobileMenu ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-mark"><Shield size={23} /></div>
          <div>
            <div className="brand-name">SENTINELOPS<span>.</span></div>
            <div className="brand-caption">AUTONOMOUS CYBER DEFENCE</div>
          </div>
        </div>

        <div className="workspace-label">COMMAND WORKSPACE</div>

        <nav className="nav-list">
          {navigation.map(item => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`nav-item ${activePage === item.name ? "active" : ""}`}
                onClick={() => {
                  setActivePage(item.name);
                  setMobileMenu(false);
                }}
              >
                <Icon size={17} />
                <span>{item.name}</span>
                {item.name === "Live Threat Monitor" && <span className="nav-live-dot" />}
              </button>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="environment-card">
            <div className="environment-head"><Radio size={14} /> SIMULATION ENVIRONMENT</div>
            <p>Controlled demo workspace</p>
            <span>Synthetic events only</span>
          </div>

          <button className="nav-item">
            <Settings size={17} />
            <span>Settings</span>
          </button>

          <div className="user-profile">
            <div className="avatar">SO</div>
            <div>
              <strong>Security Operator</strong>
              <small>Administrator</small>
            </div>
            <ChevronDown size={15} />
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <button className="mobile-menu-button" onClick={() => setMobileMenu(!mobileMenu)}>
            <Menu />
          </button>

          <div className="breadcrumb">
            SENTINELOPS <span>/</span> <strong>{activePage}</strong>
          </div>

          <div className="topbar-actions">
            <div className={`connection-pill ${online ? "online" : "offline"}`}>
              <span className="connection-dot" />
              {online ? "SYSTEM CONNECTED" : "BACKEND DISCONNECTED"}
            </div>
            <button className="icon-button" title="Search"><Search size={18} /></button>
            <button className="icon-button notification-button" title="Notifications">
              <Bell size={18} /><i />
            </button>
          </div>
        </header>

        <div className="content">
          <section className="welcome-row">
            <div>
              <div className="eyebrow">
                <span className="eyebrow-line" /> INTELLIGENCE. MEMORY. DEFENCE.
              </div>
              <h1>{activePage}</h1>
              <p>{pageDescription(activePage)}</p>
            </div>

            <div className="welcome-actions">
              <span className="simulation-tag"><Radio size={13} /> SIMULATION MODE</span>
              <button className="primary-button" onClick={runDemoIncident} disabled={busy}>
                {busy ? <RefreshCw size={15} className="spin" /> : <Play size={15} />}
                {busy ? "Processing..." : "Launch AI investigation"}
              </button>
            </div>
          </section>

          {notice && (
            <motion.div
              className="notice-bar"
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <AlertTriangle size={16} />
              <span>{notice}</span>
              <button onClick={() => setNotice("")}>Dismiss</button>
            </motion.div>
          )}

          <AnimatePresence mode="wait">
            <motion.div
              key={activePage}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.22 }}
            >
              <PageContent
                page={activePage}
                events={events}
                latestIncident={latestIncident}
                report={report}
                warRoomStatus={warRoomStatus}
                runDemoIncident={runDemoIncident}
                busy={busy}
              />
            </motion.div>
          </AnimatePresence>

          <footer className="footer">
            <span>SENTINELOPS <i>•</i> DETECT. REMEMBER. PREDICT. DEFEND. EVOLVE.</span>
            <span><LockKeyhole size={12} /> Synthetic simulation · No real security actions executed</span>
          </footer>
        </div>
      </main>

      <AnimatePresence>
        {mobileMenu && (
          <motion.div
            className="mobile-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setMobileMenu(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
