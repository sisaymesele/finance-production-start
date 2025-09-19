
class StrategyMapChoicesService:
    # Define the complete hierarchy in a single structure
    STRATEGY_MAP_HIERARCHY = {

        "Financial Perspective": {
            "Revenue Growth & Market Expansion": {
                "Expand into new geographic markets and regions": {
                    "Revenue from new markets ($)": "Total revenue generated from all new markets",
                    "Market share in new regions": "(Revenue in new regions / Total regional revenue) * 100",
                    "Customer acquisition cost in new markets ($ per customer)": "Total marketing and sales spend divided by new customers acquired",
                    "Successful market entries count": "Count of markets entered where sales targets were met"
                },
                "Increase market share in existing segments": {
                    "Market share by segment": "(Sales in segment / Total segment sales) * 100",
                    "Revenue growth vs. market growth rate": "Revenue growth rate minus market growth rate",
                    "Competitive win rate": "(Deals won / Deals competed in key accounts) * 100",
                    "Customer acquisition in target segments (count)": "Number of new customers acquired in target segments"
                },
                "Launch new products and services": {
                    "Revenue from new products/services ($)": "Revenue from all products launched in the last period",
                    "Time-to-market for new launches (days)": "Average duration from idea to market launch",
                    "Market adoption rate": "(Number of customers using new product / Total target customers) * 100",
                    "Return on R&D investment": "((Revenue from new products - R&D cost) / R&D cost) * 100"
                },
                "Develop recurring revenue streams": {
                    "Recurring revenue as percentage of total revenue": "(Recurring revenue / Total revenue) * 100",
                    "Customer subscription growth rate": "((Current subscriptions - Previous subscriptions) / Previous subscriptions) * 100",
                    "Monthly/Annual recurring revenue ($)": "Sum of recurring revenue per month or year",
                    "Customer retention rate": "(Retained recurring customers / Total recurring customers) * 100"
                },
                "Grow digital and e-commerce channels": {
                    "Online sales growth": "((Current online sales - Previous online sales) / Previous online sales) * 100",
                    "Digital channel conversion rate": "(Leads converted / Total leads through digital channels) * 100",
                    "Revenue from e-commerce channels ($)": "Total revenue generated via e-commerce platforms",
                    "Customer acquisition cost ratio (digital vs traditional)": "Digital acquisition cost divided by traditional acquisition cost"
                },
                "Strengthen cross-selling and upselling": {
                    "Cross-sell revenue growth": "((Revenue from cross-sold products - Previous revenue) / Previous revenue) * 100",
                    "Upsell conversion rate": "(Upsell transactions / Total eligible customers) * 100",
                    "Average revenue per customer ($)": "Total revenue / Total number of customers",
                    "Customer penetration rate": "(Number of customers buying multiple products / Total customers) * 100"
                },
                "Diversify revenue sources": {
                    "Revenue from new business lines ($)": "Revenue generated from newly introduced business lines",
                    "Percentage of revenue from top 3 products": "(Revenue from top 3 products / Total revenue) * 100",
                    "Number of distinct revenue streams": "Count of distinct revenue sources contributing to total revenue",
                    "Revenue concentration risk index": "Measure of dependency on top revenue sources"
                },
                "Enhance pricing strategies": {
                    "Average selling price improvement ($)": "Current average selling price - Previous average selling price",
                    "Price optimization success rate": "(Number of products priced optimally / Total products) * 100",
                    "Margin per product category": "((Revenue - Cost per category) / Revenue per category) * 100",
                    "Competitive pricing index": "Your price vs Competitor average price index"
                },
                "Deepen strategic partnerships": {
                    "Revenue from partnership channels ($)": "Revenue generated through partnerships",
                    "Number of active strategic partnerships (count)": "Count of partnerships with ongoing business activity",
                    "Partnership satisfaction score": "Average satisfaction rating from partners",
                    "Joint initiative success rate": "(Completed initiatives meeting objectives / Total initiatives) * 100"
                },
                "Improve sales force effectiveness": {
                    "Sales per representative ($)": "Revenue generated divided by number of sales representatives",
                    "Sales cycle length reduction": "((Previous cycle length - Current cycle length) / Previous cycle length) * 100",
                    "Quota attainment rate": "(Number of reps meeting quota / Total reps) * 100",
                    "Lead-to-close conversion rate": "(Leads closed / Total leads) * 100"
                }
            },
            "Cost Efficiency & Productivity": {
                "Reduce operational waste and inefficiencies": {
                    "Cost savings from waste reduction ($)": "Monetary savings achieved from reducing waste",
                    "Process efficiency improvement": "(Improved output / Baseline output) * 100",
                    "Waste reduction": "(Reduced waste / Total previous waste) * 100",
                    "Operational cost per unit produced ($)": "Total operational cost / Total units produced"
                },
                "Optimize vendor and supplier contracts": {
                    "Cost savings from contract optimization ($)": "Savings achieved through improved contract terms",
                    "Supplier performance score": "Average score from supplier performance assessments",
                    "Contract compliance rate": "(Contracts meeting compliance / Total contracts) * 100",
                    "Procurement cycle time reduction (days)": "Previous average procurement cycle - Current average cycle"
                },
                "Streamline administrative costs": {
                    "Administrative cost reduction": "((Previous admin cost - Current admin cost) / Previous admin cost) * 100",
                    "Cost per administrative transaction ($)": "Total admin cost / Number of transactions",
                    "Process automation rate": "(Automated admin processes / Total admin processes) * 100",
                    "Headcount efficiency ratio": "Output / Number of admin employees"
                },
                "Improve procurement efficiency": {
                    "Procurement cost savings": "(Cost saved through procurement improvements / Total procurement cost) * 100",
                    "Purchase order cycle time (days)": "Average time from purchase request to order fulfillment",
                    "Supplier on-time delivery rate": "(On-time deliveries / Total deliveries) * 100",
                    "Procurement process compliance rate": "(Compliant purchase orders / Total orders) * 100"
                },
                "Automate manual processes": {
                    "Processes automated": "(Number of automated processes / Total processes) * 100",
                    "Time savings from automation (hours)": "Total hours saved through automation",
                    "Error reduction rate": "(Errors reduced / Previous errors) * 100",
                    "Return on automation investment": "((Cost savings + Productivity gains) / Automation investment) * 100"
                },
                "Right-size inventory levels": {
                    "Inventory turnover ratio": "COGS / Average inventory",
                    "Inventory carrying cost reduction ($)": "Reduction in storage and holding costs",
                    "Stock-out frequency reduction": "Reduction in number of stock-outs compared to previous period",
                    "Obsolete inventory": "(Obsolete inventory / Total inventory) * 100"
                },
                "Control discretionary spending": {
                    "Discretionary spend reduction": "((Previous discretionary spend - Current) / Previous) * 100",
                    "Budget variance": "((Actual spend - Budgeted spend) / Budgeted spend) * 100",
                    "Approval cycle time reduction (days)": "Previous approval cycle time - Current cycle time",
                    "Spending policy compliance rate": "(Transactions compliant with policy / Total transactions) * 100"
                },
                "Implement energy conservation programs": {
                    "Energy cost savings": "((Previous energy cost - Current cost) / Previous cost) * 100",
                    "Carbon emissions reduction": "(CO2 emissions reduced / Previous emissions) * 100",
                    "Energy consumption per unit": "Total energy consumed / Units produced",
                    "Renewable energy usage": "(Energy from renewable sources / Total energy) * 100"
                },
                "Outsource non-core functions": {
                    "Cost savings from outsourcing ($)": "Savings from outsourcing activities vs in-house",
                    "SLA compliance": "(SLAs met / Total SLAs) * 100",
                    "Quality score of outsourced services": "Average quality rating of outsourced service",
                    "Internal resource reallocation efficiency": "(Freed internal resources / Total resources) * 100"
                },
                "Improve resource utilization": {
                    "Resource utilization": "(Used resources / Total available resources) * 100",
                    "Idle time reduction": "((Previous idle time - Current) / Previous) * 100",
                    "Capacity utilization improvement": "Current capacity utilization - Previous utilization",
                    "Productivity per resource unit": "Total output produced / Total number of resource units"
                }
            }
        },

        "Customer Perspective": {
            "Customer Acquisition & Market Reach": {
                "Increase qualified lead generation": {
                    "Number of qualified leads per month": "Count of leads meeting qualification criteria per month",
                    "Lead generation cost per channel": "Total marketing spend per channel / Number of leads generated per channel",
                    "Lead-to-opportunity conversion rate": "(Leads converted to opportunities / Total leads) * 100",
                    "Marketing qualified lead volume growth": "((Current MQL volume - Previous MQL volume) / Previous MQL volume) * 100"
                },
                "Improve conversion rates across channels": {
                    "Conversion rate by channel": "(Leads converted / Total leads per channel) * 100",
                    "Sales funnel efficiency": "(Opportunities closed / Total leads) * 100",
                    "Cost per acquisition reduction": "((Previous acquisition cost - Current acquisition cost) / Previous acquisition cost) * 100",
                    "Revenue per channel growth": "((Current revenue per channel - Previous revenue per channel) / Previous revenue per channel) * 100"
                },
                "Enhance digital marketing effectiveness": {
                    "Digital marketing ROI": "((Revenue from digital campaigns - Campaign cost) / Campaign cost) * 100",
                    "Click-through rate improvement": "((Current CTR - Previous CTR) / Previous CTR) * 100",
                    "Cost per click reduction": "((Previous CPC - Current CPC) / Previous CPC) * 100",
                    "Digital campaign conversion rate": "(Conversions / Total clicks) * 100"
                },
                "Build strong brand awareness": {
                    "Brand awareness survey": "(Surveyed awareness level / Total surveyed) * 100",
                    "Unaided brand recall": "(Respondents recalling brand without prompts / Total respondents) * 100",
                    "Social media reach and engagement": "(Total interactions on social media / Total followers) * 100",
                    "Share of voice in market": "(Brand mentions / Total market mentions) * 100"
                },
                "Target new customer segments": {
                    "Revenue from new segments": "Revenue generated from newly targeted segments",
                    "Customer acquisition rate for new segments": "(New customers acquired / Total potential customers in segment) * 100",
                    "Market penetration rate for new segments": "(Customers acquired / Total potential customers in segment) * 100",
                    "Segment growth percentage": "((Current segment revenue - Previous segment revenue) / Previous segment revenue) * 100"
                },
                "Expand into underserved markets": {
                    "Revenue from underserved markets": "Total revenue generated in underserved areas",
                    "Customer acquisition cost in new markets": "Marketing & sales spend in new markets / New customers acquired",
                    "Market share in new areas": "(Sales in new area / Total market size) * 100",
                    "Customer satisfaction in new markets": "(Sum of satisfaction ratings from new market customers / Number of respondents) * 100"
                },
                "Optimize customer onboarding": {
                    "Onboarding completion rate": "(Customers completing onboarding / Total new customers) * 100",
                    "Time to first value reduction": "Previous time to first value - Current time to first value",
                    "New customer satisfaction score": "(Sum of satisfaction ratings from new customers / Number of respondents) * 100",
                    "Onboarding cost per customer": "Total onboarding cost / Number of onboarded customers"
                },
                "Leverage customer referral programs": {
                    "Referral rate": "(Referrals / Total customers) * 100",
                    "Cost per acquired referral": "Total referral program cost / Referrals acquired",
                    "Referral program ROI": "((Revenue from referrals - Program cost) / Program cost) * 100",
                    "Customer lifetime value from referrals": "Average CLV of customers acquired via referrals"
                },
                "Improve website conversion funnels": {
                    "Website conversion rate": "(Conversions / Total website visitors) * 100",
                    "Cart abandonment rate reduction": "((Previous abandonment rate - Current abandonment rate) / Previous abandonment rate) * 100",
                    "Bounce rate improvement": "((Previous bounce rate - Current bounce rate) / Previous bounce rate) * 100",
                    "Page views per session increase": "Current average page views per session - Previous average page views per session"
                },
                "Execute targeted acquisition campaigns": {
                    "Campaign ROI": "((Revenue from campaign - Campaign cost) / Campaign cost) * 100",
                    "Customer acquisition cost per campaign": "Total campaign cost / Customers acquired from campaign",
                    "Conversion rate per campaign": "(Conversions / Total leads generated from campaign) * 100",
                    "Revenue generated from campaigns": "Total revenue attributable to specific campaigns"
                }
            },
            "Customer Satisfaction & Experience": {
                "Improve service quality standards": {
                    "Customer satisfaction score (CSAT)": "(Sum of satisfaction ratings / Number of survey respondents) * 100",
                    "Service quality index score": "((Sum of service metrics scores) / Maximum possible score) * 100",
                    "First-contact resolution rate": "(Issues resolved at first contact / Total issues) * 100",
                    "Service level agreement compliance": "(SLAs met / Total SLAs) * 100"
                },
                "Enhance customer support responsiveness": {
                    "Average response time reduction": "Previous average response time - Current average response time",
                    "Support ticket backlog reduction": "Previous backlog - Current backlog",
                    "Customer satisfaction post-support": "(Sum of satisfaction ratings post-support / Number of respondents) * 100",
                    "Resolution time improvement": "Previous average resolution time - Current average resolution time"
                },
                "Personalize customer interactions": {
                    "Personalization effectiveness score": "((Number of personalized interactions leading to desired outcome) / Total personalized interactions) * 100",
                    "Customer engagement rate improvement": "((Current engagement rate - Previous engagement rate) / Previous engagement rate) * 100",
                    "Repeat purchase rate increase": "((Current repeat purchases - Previous repeat purchases) / Previous repeat purchases) * 100",
                    "Upsell conversion rate improvement": "((Current upsell conversions - Previous upsell conversions) / Previous upsell conversions) * 100"
                },
                "Streamline customer journey mapping": {
                    "Customer effort score reduction": "((Previous effort score - Current effort score) / Previous effort score) * 100",
                    "Journey completion rate improvement": "((Current journey completions - Previous journey completions) / Previous journey completions) * 100",
                    "Touchpoint satisfaction scores": "(Sum of touchpoint satisfaction ratings / Number of touchpoints) * 100",
                    "Process step reduction in journey": "Previous number of steps - Current number of steps"
                },
                "Improve complaint resolution processes": {
                    "Complaint resolution time reduction": "((Previous resolution time - Current resolution time) / Previous resolution time) * 100",
                    "First-contact resolution rate": "(Issues resolved at first contact / Total issues) * 100",
                    "Customer satisfaction post-complaint": "(Sum of satisfaction ratings post-complaint / Number of respondents) * 100",
                    "Complaint escalation rate reduction": "((Previous escalations - Current escalations) / Previous escalations) * 100"
                },
                "Enhance after-sales service": {
                    "After-sales satisfaction score": "(Sum of satisfaction ratings after service / Number of respondents) * 100",
                    "Service follow-up completion rate": "(Follow-ups completed / Total required follow-ups) * 100",
                    "Repeat purchase rate improvement": "((Current repeat purchases - Previous repeat purchases) / Previous repeat purchases) * 100",
                    "Warranty claim resolution time": "Average time to resolve warranty claims"
                },
                "Strengthen customer communication": {
                    "Communication open rate": "(Emails opened / Total emails sent) * 100",
                    "Click-through rate improvement": "((Current CTR - Previous CTR) / Previous CTR) * 100",
                    "Customer engagement score": "((Sum of interactions per customer) / Total customers) * 100",
                    "Response rate to outreach": "(Responses received / Total outreach attempts) * 100"
                },
                "Implement customer feedback systems": {
                    "Feedback collection rate": "(Feedback collected / Total customers solicited) * 100",
                    "Actionable insights implemented": "(Implemented insights / Total insights collected) * 100",
                    "Feedback response time reduction": "((Previous response time - Current response time) / Previous response time) * 100",
                    "Customer perception of being heard": "(Sum of survey scores on being heard / Number of respondents) * 100"
                },
                "Improve product usability": {
                    "Product usability score": "(Sum of usability ratings / Number of respondents) * 100",
                    "Customer training time reduction": "((Previous training hours - Current training hours) / Previous training hours) * 100",
                    "Support calls related to usability": "(Number of calls about usability / Total support calls) * 100",
                    "Feature adoption rate improvement": "((Current adoption rate - Previous adoption rate) / Previous adoption rate) * 100"
                },
                "Enhance digital experience": {
                    "Digital experience score": "(Sum of digital experience ratings / Number of respondents) * 100",
                    "Mobile app rating improvement": "((Current rating - Previous rating) / Previous rating) * 100",
                    "Website satisfaction score": "(Sum of website satisfaction ratings / Number of respondents) * 100",
                    "Digital channel engagement rate": "(Interactions via digital channels / Total users) * 100"
                }
            },
            "Customer Loyalty & Retention": {
                "Reduce customer churn rate": {
                    "Churn rate reduction": "((Previous churn rate - Current churn rate) / Previous churn rate) * 100",
                    "Customer lifetime value improvement": "((Current CLV - Previous CLV) / Previous CLV) * 100",
                    "Revenue retention percentage": "(Revenue retained from existing customers / Total revenue) * 100",
                    "Lost customer recovery rate": "(Recovered customers / Total lost customers) * 100"
                },
                "Increase customer retention percentage": {
                    "Customer retention rate by segment": "(Retained customers / Total customers in segment) * 100",
                    "Repeat purchase rate improvement": "((Current repeat purchase rate - Previous repeat purchase rate) / Previous repeat purchase rate) * 100",
                    "Loyalty program participation rate": "(Participants / Eligible customers) * 100",
                    "Customer tenure increase": "Average tenure current period - Previous period"
                },
                "Enhance loyalty program effectiveness": {
                    "Loyalty program enrollment rate": "(Enrolled customers / Total target customers) * 100",
                    "Points redemption rate": "(Redeemed points / Total points issued) * 100",
                    "Program engagement score": "(Sum of engagement actions in program / Total participants) * 100",
                    "Retention uplift from loyalty program": "((Retention of participants - Retention of non-participants) / Retention of non-participants) * 100"
                },
                "Improve net promoter score": {
                    "NPS score improvement": "Current NPS - Previous NPS",
                    "Promoter percentage increase": "((Current promoters / Total respondents) * 100) - Previous percentage",
                    "Detractor percentage reduction": "((Previous detractors - Current detractors) / Previous detractors) * 100",
                    "NPS trend over time": "Graphical trend analysis of NPS across periods"
                },
                "Strengthen customer engagement": {
                    "Active user percentage": "(Active users / Total users) * 100",
                    "Engagement score improvement": "((Current engagement actions per user - Previous) / Previous) * 100",
                    "Interaction frequency increase": "((Current interactions - Previous interactions) / Previous interactions) * 100",
                    "Product usage depth improvement": "((Current depth metrics - Previous depth metrics) / Previous depth metrics) * 100"
                },
                "Increase renewal rates": {
                    "Contract renewal rate": "(Contracts renewed / Contracts due for renewal) * 100",
                    "Renewal revenue retention": "(Revenue from renewed contracts / Revenue from contracts due) * 100",
                    "Auto-renewal rate improvement": "((Current auto-renewals - Previous auto-renewals) / Previous auto-renewals) * 100",
                    "Renewal process satisfaction": "(Sum of satisfaction ratings with renewal process / Number of respondents) * 100"
                },
                "Improve product stickiness": {
                    "Daily active users percentage": "(DAU / Total users) * 100",
                    "Feature usage frequency": "Average usage per feature / Total users",
                    "Product dependency index": "(Sum of reliance scores per feature / Number of features) * 100",
                    "Switching cost perception": "(Sum of survey scores on perceived switching cost / Number of respondents) * 100"
                },
                "Build customer communities": {
                    "Community participation rate": "(Active community members / Total members) * 100",
                    "User-generated content volume": "Total content contributions from users",
                    "Peer-to-peer support percentage": "(Resolved support issues by peers / Total support issues) * 100",
                    "Community satisfaction score": "(Sum of community satisfaction ratings / Number of respondents) * 100"
                },
                "Enhance proactive support": {
                    "Proactive issue resolution rate": "(Proactively resolved issues / Total issues) * 100",
                    "Preventative support incidents": "Number of incidents prevented via proactive actions",
                    "Customer satisfaction proactive support": "(Sum of satisfaction ratings for proactive support / Number of respondents) * 100",
                    "Reactive ticket reduction percentage": "((Previous reactive tickets - Current reactive tickets) / Previous reactive tickets) * 100"
                },
                "Personalize retention strategies": {
                    "Personalized offer acceptance rate": "(Accepted personalized offers / Total offers) * 100",
                    "Retention campaign effectiveness": "(Retention achieved via campaign / Total targeted) * 100",
                    "Customer segment retention rates": "(Retained customers per segment / Total segment customers) * 100",
                    "Lifetime value preservation rate": "(CLV preserved via retention actions / Total CLV) * 100"
                }
            },
            "Customer Value & Relationship Management": {
                "Increase customer lifetime value": {
                    "CLV dollar amount improvement": "Current CLV - Previous CLV",
                    "Customer profitability score increase": "Current profitability score - Previous profitability score",
                    "Value per customer growth": "((Current value per customer - Previous value per customer) / Previous value per customer) * 100",
                    "Return on customer investment": "(Profit from customer / Cost to acquire & serve customer) * 100"
                },
                "Improve relationship management": {
                    "Account health score improvement": "Current health score - Previous health score",
                    "Relationship depth score": "(Sum of meaningful interactions per account / Total interactions) * 100",
                    "Strategic account retention rate": "(Strategic accounts retained / Total strategic accounts) * 100",
                    "Executive engagement frequency": "Average number of executive interactions per account"
                },
                "Enhance customer segmentation": {
                    "Segmentation accuracy percentage": "(Correctly segmented customers / Total customers) * 100",
                    "Targeting effectiveness score": "(Revenue or conversions from targeted segments / Total targeted segments) * 100",
                    "Segment-specific growth rates": "((Current segment revenue - Previous segment revenue) / Previous segment revenue) * 100",
                    "Personalization relevance score": "(Interactions meeting personalized needs / Total personalized interactions) * 100"
                },
                "Strengthen account management": {
                    "Account growth rate": "((Current account revenue - Previous account revenue) / Previous account revenue) * 100",
                    "Account penetration depth": "(Products/services used per account / Total offerings) * 100",
                    "Account manager effectiveness score": "(Sum of KPIs achieved by account manager / Total KPIs assigned) * 100",
                    "Strategic account satisfaction": "(Sum of satisfaction ratings from strategic accounts / Number of respondents) * 100"
                },
                "Develop customer success programs": {
                    "Customer success score improvement": "Current success score - Previous success score",
                    "Product adoption rate increase": "((Current adoption rate - Previous adoption rate) / Previous adoption rate) * 100",
                    "Success plan completion rate": "(Completed success plans / Total success plans) * 100",
                    "Business outcomes achieved": "(Number of outcomes achieved / Total improvement_needed outcomes) * 100"
                },
                "Improve upsell and cross-sell rates": {
                    "Upsell conversion rate": "(Upsell transactions / Eligible customers) * 100",
                    "Cross-sell revenue growth": "((Current cross-sell revenue - Previous cross-sell revenue) / Previous cross-sell revenue) * 100",
                    "Average revenue per account": "Total revenue / Total accounts",
                    "Solution adoption breadth": "(Number of solutions adopted per customer / Total solutions offered) * 100"
                },
                "Enhance customer education": {
                    "Training completion rate": "(Completed trainings / Total assigned trainings) * 100",
                    "Customer proficiency score": "(Sum of proficiency scores / Number of assessed customers) * 100",
                    "Self-service usage increase": "((Current usage - Previous usage) / Previous usage) * 100",
                    "Support ticket reduction percentage": "((Previous tickets - Current tickets) / Previous tickets) * 100"
                },
                "Build strategic customer partnerships": {
                    "Strategic partnership count": "Number of active strategic partnerships",
                    "Joint business value created": "Revenue or profit generated through partnerships",
                    "Partnership satisfaction score": "(Sum of satisfaction ratings from partners / Number of respondents) * 100",
                    "Co-innovation projects completed": "(Completed joint innovation projects / Total improvement_needed projects) * 100"
                },
                "Improve customer health scoring": {
                    "Health score accuracy percentage": "(Accurate health predictions / Total customers assessed) * 100",
                    "At-risk customer identification rate": "(Correctly identified at-risk customers / Total at-risk customers) * 100",
                    "Intervention effectiveness score": "(Revenue or retention preserved through interventions / Total interventions) * 100",
                    "Health score trend improvement": "Improvement of average health score over time"
                },
                "Develop customer advocacy programs": {
                    "Advocate identification rate": "(Identified advocates / Total customers) * 100",
                    "Referenceable customer percentage": "(Referenceable customers / Total customers) * 100",
                    "Case study completion rate": "(Completed case studies / Improvement Needed case studies) * 100",
                    "Advocate engagement score": "(Sum of engagement actions by advocates / Total advocates) * 100"
                }
            }
        },

        "Internal Process Perspective": {
            "Operational Excellence & Quality": {
                "Reduce process cycle times": {
                    "Cycle time reduction percentage": "((Previous cycle time - Current cycle time) / Previous cycle time) * 100",
                    "Process throughput improvement": "((Current throughput - Previous throughput) / Previous throughput) * 100",
                    "On-time completion rate": "(Processes completed on time / Total processes) * 100",
                    "Process efficiency score improvement": "Current process efficiency score - Previous score"
                },
                "Improve process standardization": {
                    "SOP adoption rate": "(Processes following SOP / Total processes) * 100",
                    "Process consistency score": "((Number of consistent process executions / Total executions) * 100)",
                    "Training compliance rate": "(Employees trained / Total required employees) * 100",
                    "Quality audit score improvement": "Current audit score - Previous audit score"
                },
                "Enhance quality control systems": {
                    "Quality inspection pass rate": "(Passed inspections / Total inspections) * 100",
                    "Defect detection rate improvement": "((Current detection rate - Previous) / Previous) * 100",
                    "Quality cost reduction percentage": "((Previous quality cost - Current) / Previous quality cost) * 100",
                    "Customer quality perception score": "Average rating from customer quality surveys"
                },
                "Reduce error and defect rates": {
                    "Error rate reduction percentage": "((Previous error rate - Current error rate) / Previous error rate) * 100",
                    "Defects per million reduction": "Previous defects per million - Current defects per million",
                    "Rework percentage decrease": "((Previous rework % - Current rework %) / Previous rework %) * 100",
                    "First-pass yield improvement": "Current first-pass yield - Previous first-pass yield"
                },
                "Improve supply chain efficiency": {
                    "Supply chain cycle time reduction": "((Previous cycle time - Current) / Previous cycle time) * 100",
                    "On-time delivery rate improvement": "((Current on-time deliveries - Previous) / Previous) * 100",
                    "Inventory accuracy percentage": "(Accurate inventory counts / Total inventory) * 100",
                    "Order fulfillment rate improvement": "((Current fulfilled orders - Previous) / Previous) * 100"
                },
                "Enhance inventory management": {
                    "Inventory turnover ratio improvement": "((Current turnover ratio - Previous) / Previous) * 100",
                    "Stock-out frequency reduction": "((Previous stock-outs - Current) / Previous) * 100",
                    "Inventory carrying cost reduction": "((Previous cost - Current cost) / Previous cost) * 100",
                    "Obsolete inventory percentage decrease": "((Previous obsolete % - Current) / Previous) * 100"
                },
                "Strengthen vendor performance": {
                    "Vendor performance score improvement": "Current vendor score - Previous score",
                    "Supplier on-time delivery rate": "(On-time deliveries / Total deliveries) * 100",
                    "Quality compliance rate improvement": "((Current compliance % - Previous) / Previous) * 100",
                    "Cost savings from vendor optimization": "Previous spend - Optimized spend"
                },
                "Improve asset utilization": {
                    "Asset utilization rate": "(Actual productive time / Available time) * 100",
                    "Equipment efficiency improvement": "((Current OEE - Previous OEE) / Previous OEE) * 100",
                    "Maintenance cost reduction": "((Previous maintenance cost - Current) / Previous) * 100",
                    "Uptime percentage improvement": "((Current uptime - Previous) / Previous) * 100"
                },
                "Reduce operational downtime": {
                    "Downtime hours reduction": "Previous downtime hours - Current downtime hours",
                    "Mean time between failures improvement": "Current MTBF - Previous MTBF",
                    "Mean time to repair reduction": "Previous MTTR - Current MTTR",
                    "System availability percentage": "(Uptime / Total time) * 100"
                },
                "Enhance service delivery consistency": {
                    "Service quality variance reduction": "Previous variance - Current variance",
                    "Customer experience consistency score": "((Number of consistent experiences / Total experiences) * 100)",
                    "Process standard deviation reduction": "Previous process deviation - Current deviation",
                    "Service level agreement compliance rate": "(SLAs met / Total SLAs) * 100"
                }
            },
            "Innovation & New Product Development": {
                "Accelerate time-to-market for new products": {
                    "Development cycle time reduction": "((Previous cycle time - Current) / Previous) * 100",
                    "Time from idea to launch reduction": "Previous time - Current time",
                    "Market readiness score improvement": "Current readiness score - Previous score",
                    "Project timeline adherence percentage": "(On-time milestones / Total milestones) * 100"
                },
                "Enhance R&D capabilities": {
                    "R&D investment ROI percentage": "((Revenue from R&D - R&D spend) / R&D spend) * 100",
                    "Number of patents filed": "Count of patents filed in period",
                    "Innovation pipeline strength score": "((Number of viable ideas / Total submitted ideas) * 100)",
                    "Research effectiveness index": "(Output of research / Input resources) * 100"
                },
                "Improve product design quality": {
                    "Design satisfaction score improvement": "Current satisfaction - Previous satisfaction",
                    "Number of design improvements implemented": "Count of improvements applied",
                    "Customer adoption rate": "(Adopted features / Total features) * 100",
                    "Time spent in redesign reduction": "((Previous redesign time - Current) / Previous) * 100"
                },
                "Strengthen innovation pipeline": {
                    "Pipeline conversion rate": "(Ideas converted to launch / Total ideas) * 100",
                    "Number of viable innovations": "Count of innovations passing feasibility assessment",
                    "Time through pipeline reduction": "((Previous pipeline duration - Current) / Previous) * 100",
                    "Innovation success rate": "(Successful innovations / Total launched) * 100"
                },
                "Leverage customer insights for innovation": {
                    "Customer insight utilization rate": "(Insights applied / Total collected insights) * 100",
                    "Number of insights applied to innovation": "Count of actionable insights implemented",
                    "Customer co-creation participation": "(Participants in co-creation / Total customers) * 100",
                    "Innovation relevance score improvement": "Current relevance score - Previous"
                },
                "Adopt emerging technologies": {
                    "Technology adoption rate": "(Implemented technologies / Identified emerging technologies) * 100",
                    "Number of emerging tech implementations": "Count of new tech deployed",
                    "Impact on operational efficiency": "Efficiency gain from technology adoption",
                    "Return on technology investment": "((Benefit - Cost) / Cost) * 100"
                },
                "Enhance prototyping processes": {
                    "Prototype iteration speed improvement": "((Previous iteration time - Current) / Previous) * 100",
                    "Prototype cost reduction percentage": "((Previous cost - Current) / Previous) * 100",
                    "Prototype fidelity improvement": "Current fidelity score - Previous score",
                    "Stakeholder feedback incorporation rate": "(Implemented feedback / Total feedback received) * 100"
                },
                "Improve product testing effectiveness": {
                    "Test coverage percentage improvement": "((Current coverage - Previous) / Previous) * 100",
                    "Defects caught in testing percentage": "(Defects found in test / Total defects) * 100",
                    "Testing cycle time reduction": "((Previous test duration - Current) / Previous) * 100",
                    "Customer acceptance rate improvement": "((Current acceptance rate - Previous) / Previous) * 100"
                },
                "Develop intellectual property portfolio": {
                    "Number of patents granted": "Count of patents approved",
                    "IP revenue percentage": "(Revenue from IP / Total revenue) * 100",
                    "IP portfolio value growth": "((Current value - Previous value) / Previous) * 100",
                    "Licensing deals completed": "Number of licensing agreements executed"
                },
                "Foster culture of innovation": {
                    "Employee innovation participation rate": "(Employees contributing ideas / Total employees) * 100",
                    "Number of ideas submitted": "Count of ideas submitted in period",
                    "Innovation culture survey score": "Average survey score on innovation culture",
                    "Implemented ideas percentage": "(Implemented ideas / Total submitted ideas) * 100"
                }
            }
        },

        "Learning & Growth Perspective": {
            "People & Culture Development": {
                "Improve employee engagement": {
                    "Employee engagement survey score": "Average survey score across engagement questions",
                    "Voluntary turnover rate reduction": "((Previous voluntary turnover - current) / previous) * 100",
                    "Employee net promoter score": "Promoters % - Detractors %",
                    "Engagement action plan completion rate": "(Completed action plans / total plans) * 100"
                },
                "Enhance workplace culture": {
                    "Culture survey score improvement": "Current culture survey score - previous score",
                    "Values alignment percentage": "(Employees aligned with core values / total employees) * 100",
                    "Employee satisfaction score": "Average satisfaction survey score",
                    "Organizational health index": "Weighted index of culture, engagement, and satisfaction metrics"
                },
                "Strengthen diversity and inclusion": {
                    "Diversity representation at all levels": "(Employees from diverse groups / total employees) * 100",
                    "Inclusion index score": "Weighted score of inclusion survey metrics",
                    "Belongingness survey results": "Average survey score",
                    "Diverse promotion rate": "(Promotions of diverse employees / total promotions) * 100"
                },
                "Improve work-life balance": {
                    "Employee work-life balance score": "Average survey score on balance metrics",
                    "Flexible work arrangement participation": "(Employees using flexible arrangements / total employees) * 100",
                    "Overtime hours reduction percentage": "((Previous overtime hours - current) / previous) * 100",
                    "Employee burnout rate reduction": "((Previous burnout % - current) / previous) * 100"
                },
                "Enhance employee wellbeing": {
                    "Wellbeing program participation rate": "(Participants / total employees) * 100",
                    "Healthcare cost trend reduction": "((Previous cost - current cost) / previous cost) * 100",
                    "Employee stress level reduction": "((Previous stress score - current) / previous) * 100",
                    "Wellbeing index score improvement": "Current wellbeing index - previous"
                },
                "Strengthen internal communication": {
                    "Internal communication effectiveness score": "Weighted survey score",
                    "Message open and read rates": "(Opened/read messages / total messages) * 100",
                    "Employee feedback response rate": "(Responded feedback / total feedback) * 100",
                    "Communication channel utilization": "(Usage of available channels / total channels) * 100"
                },
                "Improve recognition programs": {
                    "Recognition program participation rate": "(Participants / total employees) * 100",
                    "Employee recognition frequency": "Number of recognitions / total employees",
                    "Recognition program satisfaction score": "Average satisfaction survey score",
                    "Peer-to-peer recognition percentage": "(Peer recognitions / total recognitions) * 100"
                },
                "Enhance collaboration across teams": {
                    "Cross-functional project success rate": "(Successful projects / total projects) * 100",
                    "Collaboration tool adoption rate": "(Users of collaboration tools / total employees) * 100",
                    "Inter-departmental satisfaction score": "Average survey score",
                    "Knowledge sharing frequency": "Number of knowledge sharing sessions per period"
                },
                "Foster innovation culture": {
                    "Idea submission rate per employee": "Total ideas submitted / total employees",
                    "Innovation program participation": "(Participants in innovation programs / total employees) * 100",
                    "Failed project learning application rate": "(Learnings applied / failed projects) * 100",
                    "Risk-taking encouragement score": "Survey score on risk-taking perception"
                },
                "Improve change management": {
                    "Change initiative success rate": "(Successful initiatives / total initiatives) * 100",
                    "Employee change readiness score": "Average readiness survey score",
                    "Change adoption rate": "(Employees adopting change / total impacted) * 100",
                    "Resistance to change reduction": "((Previous resistance % - current) / previous) * 100"
                }
            },
            "Leadership & Talent Management": {
                "Enhance leadership development": {
                    "Leadership competency score improvement": "Current score - previous score",
                    "Leadership program completion rate": "(Completed participants / total participants) * 100",
                    "360-degree feedback score improvement": "Current 360 feedback - previous feedback",
                    "Leadership bench strength index": "Weighted index of ready-now leaders"
                },
                "Improve succession planning": {
                    "Succession plan coverage percentage": "(Key positions with plan / total key positions) * 100",
                    "Key position readiness score": "Weighted readiness score of successors",
                    "Internal promotion rate": "(Internal promotions / total promotions) * 100",
                    "Succession plan effectiveness rating": "Survey/metric rating of plan success"
                },
                "Strengthen talent acquisition": {
                    "Time-to-fill open positions": "Average days from job posting to hire",
                    "Quality of hire index": "Weighted score of performance, retention, and engagement of new hires",
                    "Candidate experience score": "Average survey score from candidates",
                    "Diverse hiring percentage": "(Diverse hires / total hires) * 100"
                },
                "Enhance performance management": {
                    "Goal achievement rate": "(Goals achieved / total goals) * 100",
                    "Performance review completion rate": "(Completed reviews / total employees) * 100",
                    "Feedback quality score": "Average quality score of feedback sessions",
                    "Performance improvement plan success rate": "(Successful PIPs / total PIPs) * 100"
                },
                "Improve coaching and mentoring": {
                    "Coaching program participation rate": "(Participants / total employees) * 100",
                    "Mentoring relationship satisfaction": "Average satisfaction score",
                    "Skill development progress rate": "(Skills achieved / improvement_needed skills) * 100",
                    "Coaching effectiveness score": "Survey/metric score on coaching impact"
                },
                "Develop future leaders": {
                    "High-potential identification rate": "(High-potential employees / total employees) * 100",
                    "Leadership program success rate": "(Successful program graduates / total participants) * 100",
                    "Ready-now candidates for key roles": "Count of ready-now employees",
                    "Leadership pipeline diversity percentage": "(Diverse leaders in pipeline / total leaders) * 100"
                },
                "Enhance executive development": {
                    "Executive competency score improvement": "Current score - previous score",
                    "Strategic thinking capability assessment": "Weighted score from assessment",
                    "Executive team effectiveness score": "Survey or metric score",
                    "Board evaluation of executive performance": "Average board evaluation score"
                },
                "Improve talent retention": {
                    "Regrettable attrition rate reduction": "((Previous regrettable attrition % - current) / previous) * 100",
                    "Key talent retention percentage": "(Key talent retained / total key talent) * 100",
                    "Exit interview satisfaction score": "Average satisfaction score from exits",
                    "Retention risk identification rate": "(Identified retention risks / total employees) * 100"
                },
                "Strengthen competency frameworks": {
                    "Competency model adoption rate": "(Employees assessed / total employees) * 100",
                    "Skill gap reduction percentage": "((Previous gap - current gap) / previous) * 100",
                    "Competency assessment completion rate": "(Completed assessments / total required) * 100",
                    "Role-specific competency alignment": "(Employees meeting role competency / total employees) * 100"
                },
                "Enhance leadership pipeline": {
                    "Pipeline readiness score improvement": "Current score - previous score",
                    "Internal fill rate for leadership roles": "(Internal fills / total leadership openings) * 100",
                    "Leadership development program ROI": "((Benefit - cost) / cost) * 100",
                    "Pipeline diversity and inclusion metrics": "(Diverse employees in pipeline / total pipeline) * 100"
                }
            },
            "Technology & Digital Enablement": {
                "Enhance digital transformation": {
                    "Digital maturity score improvement": "Current maturity score - previous score",
                    "Digital initiative ROI percentage": "((Benefit - cost) / cost) * 100",
                    "Digital process adoption rate": "(Processes digitized / total processes) * 100",
                    "Digital revenue contribution percentage": "(Revenue from digital channels / total revenue) * 100"
                },
                "Improve technology infrastructure": {
                    "System uptime percentage": "(Uptime / total operational time) * 100",
                    "Infrastructure cost efficiency": "Output / infrastructure cost",
                    "Technology refresh cycle compliance": "(Systems refreshed on schedule / total systems) * 100",
                    "Infrastructure scalability score": "Weighted score of scalability metrics"
                },
                "Strengthen cybersecurity measures": {
                    "Security incident reduction percentage": "((Previous incidents - current) / previous) * 100",
                    "Vulnerability remediation time": "Average time to remediate vulnerabilities",
                    "Security compliance score": "Weighted compliance score",
                    "Phishing test success rate improvement": "((Current success rate - previous) / previous) * 100"
                },
                "Enhance data analytics capabilities": {
                    "Data-driven decision percentage": "(Decisions using data / total decisions) * 100",
                    "Analytics adoption rate": "(Users leveraging analytics / total employees) * 100",
                    "Insight-to-action time reduction": "((Previous time - current time) / previous) * 100",
                    "Data quality score improvement": "Current data quality score - previous"
                },
                "Improve system integration": {
                    "Integration defect rate reduction": "((Previous defects - current) / previous) * 100",
                    "Data consistency across systems": "(Consistent data points / total data points) * 100",
                    "API utilization rate": "(API calls used / total potential calls) * 100",
                    "Integration maintenance cost reduction": "((Previous cost - current) / previous) * 100"
                },
                "Enhance automation capabilities": {
                    "Process automation rate": "(Automated processes / total processes) * 100",
                    "Automation ROI percentage": "((Benefit - cost) / cost) * 100",
                    "Manual process reduction percentage": "((Previous manual processes - current) / previous) * 100",
                    "Automation scalability score": "Weighted score of automation scalability"
                },
                "Improve IT service delivery": {
                    "IT service desk satisfaction score": "Average survey score from users",
                    "Mean time to resolution reduction": "((Previous MTTR - current MTTR) / previous) * 100",
                    "Service level agreement compliance rate": "(SLAs met / total SLAs) * 100",
                    "IT project delivery on time percentage": "(Projects delivered on time / total projects) * 100"
                },
                "Strengthen cloud adoption": {
                    "Cloud migration completion percentage": "(Completed migrations / total improvement_needed) * 100",
                    "Cloud cost optimization percentage": "((Previous cost - current) / previous) * 100",
                    "Cloud security compliance score": "Weighted score of cloud security compliance",
                    "Cloud performance reliability percentage": "(Actual cloud uptime / total uptime) * 100"
                },
                "Enhance mobile solutions": {
                    "Mobile app adoption rate": "(Active users / total users) * 100",
                    "Mobile channel satisfaction score": "Average survey score",
                    "Mobile transaction completion rate": "(Completed transactions / total attempted) * 100",
                    "Mobile security incident reduction": "((Previous incidents - current) / previous) * 100"
                },
                "Improve digital literacy": {
                    "Digital skills assessment score": "Average score on digital skill assessments",
                    "Training completion rate": "(Completed training / total required) * 100",
                    "Digital tool adoption rate": "(Users using digital tools / total employees) * 100",
                    "Self-service capability utilization": "(Usage of self-service tools / total potential usage) * 100"
                }
            },
            "Knowledge, Collaboration & Innovation Capacity": {
                "Enhance knowledge management": {
                    "Knowledge base utilization rate": "(KB accesses / total employees) * 100",
                    "Content findability score improvement": "Current score - previous score",
                    "Knowledge sharing frequency": "Number of knowledge sharing events per period",
                    "Reduced duplicate work percentage": "((Previous duplicates - current) / previous) * 100"
                },
                "Improve collaboration tools": {
                    "Tool adoption rate": "(Users using collaboration tools / total employees) * 100",
                    "Collaboration satisfaction score": "Average survey score",
                    "Remote collaboration effectiveness": "Weighted score of remote collaboration success",
                    "Cross-functional project success rate": "(Successful projects / total projects) * 100"
                },
                "Strengthen learning organization": {
                    "Average learning hours per employee": "Total learning hours / total employees",
                    "Training completion rate": "(Completed trainings / total assigned) * 100",
                    "Skill competency improvement percentage": "((Current competency - previous) / previous) * 100",
                    "Employee learning satisfaction score": "Average survey score"
                },
                "Enhance innovation processes": {
                    "Implemented innovations count": "Number of innovations implemented",
                    "Time-to-implementation for innovations": "Average time from idea to implementation",
                    "Innovation ROI percentage": "((Benefit - cost) / cost) * 100",
                    "Employee participation in innovation programs": "(Participants / total employees) * 100"
                },
                "Improve knowledge sharing": {
                    "Knowledge repository usage rate": "(Repository accesses / total employees) * 100",
                    "Frequency of knowledge sharing sessions": "Number of sessions per period",
                    "Employee satisfaction with knowledge access": "Average survey score",
                    "Reduction in duplicated tasks percentage": "((Previous duplicated tasks - current) / previous) * 100"
                },
                "Strengthen research capabilities": {
                    "Completed research projects": "Count of research projects finished",
                    "Research outcomes implemented percentage": "(Implemented outcomes / total outcomes) * 100",
                    "Research budget utilization efficiency": "(Actual spend / budgeted spend) * 100",
                    "External research collaboration count": "Count of collaborations"
                },
                "Enhance cross-functional collaboration": {
                    "Cross-functional project success rate": "(Successful projects / total projects) * 100",
                    "Participation in cross-team initiatives": "(Employees involved / total employees) * 100",
                    "Collaboration survey score": "Average survey score",
                    "Number of knowledge transfer sessions": "Total sessions conducted"
                },
                "Improve idea management": {
                    "Idea submission count": "Total ideas submitted",
                    "Approved idea implementation rate": "(Implemented ideas / approved ideas) * 100",
                    "Impact score of implemented ideas": "Weighted impact score of ideas",
                    "Employee engagement in idea programs": "(Participants / total employees) * 100"
                },
                "Strengthen continuous improvement": {
                    "Number of CI initiatives": "Total CI initiatives implemented",
                    "Process improvement impact score": "Weighted score of improvements",
                    "Employee engagement in CI programs": "(Participants / total employees) * 100",
                    "Efficiency gain percentage from CI": "((Previous process inefficiency - current) / previous) * 100"
                },
                "Enhance organizational learning": {
                    "Learning program adoption rate": "(Employees using learning programs / total employees) * 100",
                    "Skills competency improvement percentage": "((Current skill competency - previous) / previous) * 100",
                    "Employee satisfaction with learning": "Average survey score",
                    "Application of learning in business outcomes": "(Measured application of learning in tasks / total expected application) * 100"
                },
            },
        },
    }

    # Getters for forms
    @classmethod
    def get_perspective_choices(cls):
        return [(p, p) for p in cls.STRATEGY_MAP_HIERARCHY.keys()]

    @classmethod
    def get_pillar_choices(cls, perspective):
        return [(p, p) for p in cls.STRATEGY_MAP_HIERARCHY.get(perspective, {}).keys()]

    @classmethod
    def get_objective_choices(cls, perspective, pillar):
        return [(o, o) for o in cls.STRATEGY_MAP_HIERARCHY.get(perspective, {}).get(pillar, {}).keys()]

    @classmethod
    def get_kpi_choices(cls, perspective, pillar, objective):
        return [(kpi, kpi) for kpi in
                cls.STRATEGY_MAP_HIERARCHY.get(perspective, {}).get(pillar, {}).get(objective, {}).keys()]

    @classmethod
    def get_formula(cls, perspective, pillar, objective, kpi):
        return cls.STRATEGY_MAP_HIERARCHY.get(perspective, {}).get(pillar, {}).get(objective, {}).get(kpi, "")