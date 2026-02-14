/**
 * Signal-to-Site OpenClaw Plugin
 *
 * The "wow" factor: Text a company name, get a branded landing page in 60 seconds.
 *
 * This plugin:
 * 1. Detects company + signal mentions in chat
 * 2. Orchestrates browser automation for research
 * 3. Generates personalized landing pages + outreach
 * 4. Deploys live and delivers results to user
 */

import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load prompt templates
const loadPrompt = (name) => {
  try {
    return readFileSync(join(__dirname, "..", "skills", "signal-to-site", "prompts", `${name}.md`), "utf-8");
  } catch {
    return "";
  }
};

export default function signalToSitePlugin(api) {
  const config = api.config || {};

  // Default configuration
  const settings = {
    your_company: config.your_company || process.env.YOUR_COMPANY_NAME || "Your Company",
    your_value_prop: config.your_value_prop || process.env.YOUR_VALUE_PROP || "We help companies grow",
    sender_name: config.sender_name || process.env.SENDER_NAME || "Alex",
    sender_email: config.sender_email || process.env.SENDER_EMAIL || "",
    calendly_url: config.calendly_url || process.env.CTA_URL || "https://calendly.com/demo",
    deploy_to: config.deploy_to || "local",
    netlify_token: config.netlify_token || process.env.NETLIFY_TOKEN || "",
    auto_send: config.auto_send || false,
  };

  // ============================================================
  // SLASH COMMAND: /signal-to-site
  // ============================================================
  api.registerCommand({
    name: "signal-to-site",
    description: "Generate hyper-personalized landing page + outreach in 60 seconds",
    usage: "/signal-to-site <domain> [signal]",
    examples: [
      "/signal-to-site stripe.com hiring Head of Sales",
      "/signal-to-site anthropic.com raised Series C",
      "/signal-to-site linear.app",
    ],
    handler: async (ctx) => {
      const args = ctx.args || [];
      if (args.length === 0) {
        return {
          text: `**Signal-to-Site** 🎯

Transform any company into personalized outreach in 60 seconds.

**Usage:**
\`/signal-to-site <domain> [signal]\`

**Examples:**
• \`/signal-to-site stripe.com hiring Head of Sales\`
• \`/signal-to-site anthropic.com raised Series C\`
• \`/signal-to-site linear.app\` (I'll research and suggest a signal)

**What I'll create:**
• 🎨 Landing page using their exact brand colors
• 📧 Email referencing specific content from their site
• 💼 LinkedIn message under 300 chars

Ready to try? Give me a domain!`,
        };
      }

      const domain = args[0].replace(/^https?:\/\//, "").replace(/\/$/, "");
      const signal = args.slice(1).join(" ") || "general outreach";

      // Trigger the research flow
      return {
        text: `🔍 **Starting Signal-to-Site for ${domain}**

Signal: ${signal}

I'll now:
1. Visit their website and extract brand identity
2. Find specific hooks for personalization
3. Generate a branded landing page
4. Draft personalized outreach

Give me 60 seconds... ⏱️`,
        // This triggers the agent to continue with the research
        continue: true,
        systemPrompt: buildOrchestratorPrompt(domain, signal, settings),
      };
    },
  });

  // ============================================================
  // AUTO-DETECT: Company mentions in natural chat
  // ============================================================
  api.registerHook({
    event: "before_inference",
    handler: async (ctx) => {
      const message = ctx.message?.text || "";

      // Detect patterns like "check out acme.com" or "acme.com is hiring"
      const companyPattern = /(?:check out|look at|research|analyze)?\s*([a-z0-9-]+\.[a-z]{2,})\s*(?:is|are|just|recently)?\s*(hiring|raised|funding|growing|launched)?/i;
      const match = message.match(companyPattern);

      if (match) {
        const domain = match[1];
        const signal = match[2] || "";

        // Inject signal-to-site context
        ctx.systemPromptAppend = `
[SIGNAL-TO-SITE DETECTED]
The user mentioned ${domain}${signal ? ` with signal: ${signal}` : ""}.
You can offer to run signal-to-site research on this company.
If they want full outreach, use the browser to research and generate assets.
`;
      }

      return ctx;
    },
  });

  // ============================================================
  // TOOL: signal_to_site_research
  // Exposed for LLM tool use
  // ============================================================
  api.registerTool({
    name: "signal_to_site_research",
    description: `Research a company website and extract brand identity for personalized outreach.
Use this when you need to:
- Extract a company's brand colors, tagline, and tone
- Find specific hooks for personalization (case studies, team members)
- Prepare data for landing page generation`,
    parameters: {
      type: "object",
      properties: {
        domain: {
          type: "string",
          description: "Company domain (e.g., 'stripe.com')",
        },
        signal_type: {
          type: "string",
          enum: ["hiring", "funding", "custom"],
          description: "Type of signal",
        },
        signal_details: {
          type: "string",
          description: "Specific signal details (e.g., 'Head of Marketing')",
        },
      },
      required: ["domain"],
    },
    handler: async (params, ctx) => {
      // This returns instructions for the agent to use browser tool
      return {
        instructions: buildResearchInstructions(params.domain, params.signal_type, params.signal_details),
        note: "Use the browser tool to execute these research steps, then compile the brand profile.",
      };
    },
  });

  // ============================================================
  // TOOL: signal_to_site_generate
  // Generate landing page and outreach from brand profile
  // ============================================================
  api.registerTool({
    name: "signal_to_site_generate",
    description: `Generate personalized landing page and outreach from a brand profile.
Use this after researching a company to create:
- HTML landing page with their brand colors
- Personalized email draft
- LinkedIn connection message`,
    parameters: {
      type: "object",
      properties: {
        brand_profile: {
          type: "object",
          description: "Brand profile from research step",
        },
        output_dir: {
          type: "string",
          description: "Directory to save generated files",
          default: "./output",
        },
      },
      required: ["brand_profile"],
    },
    handler: async (params, ctx) => {
      const { brand_profile, output_dir = "./output" } = params;

      return {
        instructions: buildGenerationInstructions(brand_profile, output_dir, settings),
        note: "Generate the HTML page and outreach content, then save to files.",
      };
    },
  });

  // ============================================================
  // TOOL: signal_to_site_deploy
  // Deploy generated page to Netlify
  // ============================================================
  api.registerTool({
    name: "signal_to_site_deploy",
    description: "Deploy a generated landing page to Netlify and return the live URL.",
    parameters: {
      type: "object",
      properties: {
        page_dir: {
          type: "string",
          description: "Directory containing the page to deploy",
        },
        site_name: {
          type: "string",
          description: "Netlify site name (optional)",
        },
      },
      required: ["page_dir"],
    },
    handler: async (params, ctx) => {
      if (!settings.netlify_token) {
        return {
          success: false,
          error: "Netlify token not configured. Page saved locally.",
          local_path: params.page_dir,
        };
      }

      return {
        instructions: `Deploy the page using Netlify CLI:
\`\`\`bash
cd ${params.page_dir}
netlify deploy --prod --dir=.
\`\`\`

Return the deployed URL to the user.`,
      };
    },
  });

  // ============================================================
  // GATEWAY RPC: For external triggers (webhooks, Linkt)
  // ============================================================
  api.registerGatewayMethod({
    name: "signalToSite.process",
    description: "Process a signal from external source (Linkt, webhook)",
    handler: async (params) => {
      const { domain, signal_type, signal_details, channel_id } = params;

      // Queue the processing
      return {
        status: "queued",
        message: `Processing ${domain} with signal: ${signal_type}`,
        // This would trigger a sub-agent to do the work
      };
    },
  });

  // ============================================================
  // HELPER FUNCTIONS
  // ============================================================

  function buildOrchestratorPrompt(domain, signal, settings) {
    const orchestratePrompt = loadPrompt("orchestrate");

    return `${orchestratePrompt}

## Current Task

**Domain**: ${domain}
**Signal**: ${signal}

**Your Settings**:
- Your Company: ${settings.your_company}
- Value Prop: ${settings.your_value_prop}
- Sender: ${settings.sender_name}
- CTA URL: ${settings.calendly_url}

Now execute the research and generation flow. Use the browser tool to visit ${domain}, extract their brand, and create personalized assets.

Start by navigating to https://${domain} and taking a screenshot.`;
  }

  function buildResearchInstructions(domain, signalType, signalDetails) {
    return `## Research Instructions for ${domain}

### Step 1: Homepage (required)
\`\`\`
browser.navigate("https://${domain}")
browser.screenshot({ fullPage: true })
browser.extractText()
\`\`\`

Extract:
- Primary color (look at buttons, headers)
- Secondary color (accents, links)
- Main headline/tagline
- Key navigation items

### Step 2: About Page (if exists)
\`\`\`
browser.navigate("https://${domain}/about")
browser.extractText()
\`\`\`

Extract:
- Company description
- Team members (especially founders/C-suite)
- Company size/stage

### Step 3: Quick Social Proof Scan
Check /customers or /case-studies if visible in nav.
Just grab 1-2 customer names or case study titles.

### Compile Brand Profile
After research, compile:
\`\`\`json
{
  "company": {
    "name": "...",
    "domain": "${domain}",
    "tagline": "...",
    "description": "..."
  },
  "brand": {
    "primary_color": "#...",
    "secondary_color": "#...",
    "tone": "professional|casual|technical"
  },
  "hooks": {
    "team_member": "...",
    "case_study": "...",
    "specific_detail": "..."
  },
  "signal": {
    "type": "${signalType || "custom"}",
    "details": "${signalDetails || ""}"
  }
}
\`\`\`

Speed target: 30 seconds total for research.`;
  }

  function buildGenerationInstructions(brandProfile, outputDir, settings) {
    const bp = brandProfile || {};
    const company = bp.company || {};
    const brand = bp.brand || {};
    const hooks = bp.hooks || {};
    const signal = bp.signal || {};

    return `## Generate Personalized Assets

### Landing Page

Create an HTML file with:

**Colors**:
- Primary: ${brand.primary_color || "#2563eb"}
- Secondary: ${brand.secondary_color || "#1e293b"}

**Content**:
- Badge: "Built for ${company.name || "Your Company"}"
- Headline: Connect their signal (${signal.type}: ${signal.details}) to your value prop
- Specific hook: Reference "${hooks.specific_detail || hooks.case_study || "their recent work"}"
- CTA: "${settings.calendly_url}"

**Save to**: ${outputDir}/${company.domain?.replace(/\./g, "-") || "company"}/index.html

### Email

**Subject**: Reference something specific (under 50 chars)
**Body**:
- Open with specific observation about their company
- Connect to signal (${signal.type})
- Your value prop: ${settings.your_value_prop}
- Include page link
- Under 150 words
- Sign: ${settings.sender_name}

### LinkedIn (300 chars max)

Short, specific reference + connection request.

### Save All Assets

Save to ${outputDir}/:
- index.html (the landing page)
- email.md (the email draft)
- linkedin.txt (the connection message)
- brand-profile.json (for reference)`;
  }
}

// Export for direct CLI usage if needed
export { signalToSitePlugin as default };
