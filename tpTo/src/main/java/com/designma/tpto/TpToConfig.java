package com.designma.tpto;

import net.minecraftforge.common.config.Config;
import net.minecraftforge.common.config.ConfigManager;
import net.minecraftforge.fml.client.event.ConfigChangedEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

@Config(modid = TpToMod.MODID)
public class TpToConfig {
    @Config.Comment("The amount of max XP levels required to use the /tpto command.")
    @Config.RangeInt(min = 1, max = 100)
    public static int xpCost = 8;

    @Config.Comment("Distance between players to apply max XP cost.")
    @Config.RangeDouble(min = 1, max = 2000)
    public static double maxDistance = 2000;

    @Mod.EventBusSubscriber(modid = TpToMod.MODID)
    public static class ConfigHandler {
        @SubscribeEvent
        public static void onConfigChanged(ConfigChangedEvent.OnConfigChangedEvent event) {
            if (event.getModID().equals(TpToMod.MODID)) {
                ConfigManager.sync(TpToMod.MODID, net.minecraftforge.common.config.Config.Type.INSTANCE);
            }
        }
    }
}